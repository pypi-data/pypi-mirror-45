
import gzip
import sys
import argparse
import configparser
from itertools import zip_longest


def parse_prep(prepname, prepfile):
    """Gets parameters from specified prep name and config file."""

    preps = configparser.ConfigParser()
    preps.read(prepfile)
    return preps[prepname.upper()]


def getread(fastq_file):
    """(Iter) slices fastq into 4-line reads."""
    args = [iter(fastq_file)] * 4
    return zip_longest(*args, fillvalue=None)


def extract_umis(reads, umi_locs, umi_lens):
    """Gets the UMI from a read."""
    umis = []

	#Iterate through (umi_loc, umi_len) pairs in list of tuple pairs
    for umi_loc, umi_len in zip(umi_locs, umi_lens):
        read = reads[int(umi_loc) - 1]
        umis.append(read[0:int(umi_len)])

    return umis


def verify_spacer(reads, umis, spacer_seq):
    """Returns true if spacer is present."""
    for read in reads:
        for umi in umis:
            if umi in read:
                if not read.split(umi)[1].startswith(spacer_seq):
                    return False
    return True


def reheader_fastqs(r1_file, r2_file, r3_file, output_path, prepname, prepfile):
    """
    (Main) Reheaders fastq files according to specified library prep.
    - removes reads without a valid spacer (if applicable)
    - gzip module is very slow, consider subprocess (at the cost of compatibility)
    """
    prep = parse_prep(prepname, prepfile)

    num_reads = int(prep['INPUT_READS'])
    actual_reads = int(prep['OUTPUT_READS'])
    umi_locs = [str(x) for x in prep['UMI_LOCS'].split(',')]
    umi_lens = [int(x) for x in prep['UMI_LENS'].split(',')]
    spacer = bool(prep['SPACER'])
    
    ##Handle SPACER=FALSE condition
    if prep['SPACER_SEQ'] is not None: 
        spacer_seq = str(prep['SPACER_SEQ'])
    else:
        spacer_seq = None
    
	#Read FASTQ in text mode
    r1 = gzip.open(r1_file, "rt")
    r2 = gzip.open(r2_file, "rt") if num_reads > 1 else None
    r3 = gzip.open(r3_file, "rt") if num_reads > 2 else None

    r1_writer = gzip.open(output_path + "_R1.fastq.gz", "wt")
    r2_writer = gzip.open(output_path + "_R2.fastq.gz",
                          "wt") if actual_reads > 1 else None

    spacer_len_r1 = 0
    spacer_len_r2 = 0

    if spacer:
        spacer_len_r1 = len(spacer_seq)

        if len(umi_locs) > 1:
            spacer_len_r2 = len(spacer_seq)

    umi_len_r1 = umi_lens[0]

    if len(umi_lens) > 1:
        umi_len_r2 = umi_lens[1]
    else:
        umi_len_r2 = 0

    print("Preprocessing reads...")

    if num_reads == 3:

        if actual_reads == 2:

            for read1, read2, read3 in zip(getread(r1), getread(r2), getread(r3)):

                umis = extract_umis(
                    [read1[1], read2[1], read3[1]], umi_locs, umi_lens)

                read_name1, rest1 = read1[0].rstrip().split(' ')
                read_name2, rest2 = read3[0].rstrip().split(' ')

                r1_writer.write(read_name1 + ":" +
                                umis[0] + " " + rest1 + "\n")
                r1_writer.write(read1[1])
                r1_writer.write(read1[2])
                r1_writer.write(read1[3])

                r2_writer.write(read_name2 + ":" +
                                umis[0] + " " + rest2 + "\n")
                r2_writer.write(read3[1])
                r2_writer.write(read3[2])
                r2_writer.write(read3[3])

        else:
            raise ValueError("Invalid configuration of reads/actual reads.")

    elif num_reads == 2:

        if actual_reads == 2:

            for read1, read2 in zip(getread(r1), getread(r2)):

                umis = extract_umis([read1[1], read2[1]], umi_locs, umi_lens)

                if spacer and not verify_spacer([read1[1], read2[1]], umis, spacer_seq):
                    next

                read_name1, rest1 = read1[0].rstrip().split(' ')
                read_name2, rest2 = read2[0].rstrip().split(' ')

                r1_writer.write(read_name1 + ":" +
                                ''.join(umis) + " " + rest1 + "\n")
                r1_writer.write(read1[1][umi_len_r1 + spacer_len_r1:])
                r1_writer.write(read1[2])
                r1_writer.write(read1[3][umi_len_r1 + spacer_len_r1:])

                r2_writer.write(read_name2 + ":" +
                                ''.join(umis) + " " + rest2 + "\n")
                r2_writer.write(read2[1][umi_len_r2 + spacer_len_r2:])
                r2_writer.write(read2[2])
                r2_writer.write(read2[3][umi_len_r2 + spacer_len_r2:])

        elif actual_reads == 1:

            for read1, read2 in zip(getread(r1), getread(r2)):

                umis = extract_umis([read1[1], read2[1]], umi_locs, umi_lens)
                read_name1, rest1 = read1[0].rstrip().split(' ')
                r1_writer.write(read_name1 + ":" +
                                umis[0] + " " + rest1 + "\n")
                r1_writer.write(read1[1])
                r1_writer.write(read1[2])
                r1_writer.write(read1[3])

        else:
            raise ValueError("Invalid configuration of reads/actual reads.")

    else:

        if actual_reads == 1:

            for read1 in getread(r1):

                umis = extract_umis([read1[1]], umi_locs, umi_lens)

                if spacer:

                    if not verify_spacer([read1[1], read2[1]], umis, spacer_seq):
                        next

                    spacer_len = len(spacer_seq)

                else:
                    spacer_len = 0

                read_name1, rest1 = read1[0].rstrip().split(' ')
                r1_writer.write(read_name1 + ":" +
                                umis[0] + " " + rest1 + "\n")
                r1_writer.write(read1[1][umi_len_r1 + spacer_len_r1:])
                r1_writer.write(read1[2])
                r1_writer.write(read1[3][umi_len_r1 + spacer_len_r1:])

        else:
            raise ValueError("Invalid configuration of reads/actual reads.")

    r1.close()
    if r2:
        r2.close() 
    if r3:
        r3.close() 

    r1_writer.close()
    if r2_writer:
        r2_writer.close() 

    print("Complete. Output written to {}.".format(output_path))


if __name__ == '__main__':

    # Argument parsing
    parser = argparse.ArgumentParser()
    parser.add_argument('-r1', '--read1', help='Path to first FASTQ file.', required=True)
    parser.add_argument('-r2', '--read2', help='Path to second FASTQ file, if necessary.')
    parser.add_argument('-r3', '--read3', help='Path to third FASTQ file, if necessary.')
    parser.add_argument('-p',  '--prepname', help='Name of library prep to  use (defined in library_prep_types.ini).', required=True)
    parser.add_argument('-pf', '--prepfile', help='Path to your library_prep_types.ini file.', required=True)
    parser.add_argument('-o',  '--output_path', help='Path to write new files to.', required=True)

    args = parser.parse_args()

    r1_file = args.read1
    r2_file = args.read2
    r3_file = args.read3
    output_path = args.output_path
    prepname = args.prepname
    prepfile = args.prepfile

    # Preprocess (reheader fastq files)
    reheader_fastqs(r1_file, r2_file, r3_file, output_path, prepname, prepfile)

