import os
import sys
import matplotlib
matplotlib.use('Agg')
import os
import sys
import pysam
import configparser
import argparse
import operator
import functools
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import re
import csv
import fnmatch
import itertools
from matplotlib.pyplot import figure

#import plotly.graph_objs as go
#import plotly.offline as off

"""
/src/create_plots.py 
=========================================
Purpose:

Script contains sub-functions for Debarcer's 'plot' sub-process.

Author: Isha Warikoo
Copyright (c) 2018 GSI, Ontario Institute for Cancer Research

"""


#Umi plots
def check_file(file_name, extension):
	file_exists = file_name.exists()
	name = file_name.split('/')[-1]
	ext = name.split('.')[-1]

	if file_exists and ext == extension:
		return True
	else:
		return False


def create_umi_dfs(file_name):

	f = file_name.split('/')[-1]
	name = f.split('.')[0]

	headers=['CHR', 'START', 'END', 'PTU', 'CTU', 'CHILD_NUMS', 'FREQ_PARENTS']
	df_headers=['INTVL', 'PTU', 'CTU', 'CHILD_NUMS', 'FREQ_PARENTS', 'INTVL_SIZE', 'CP']
	region, total_pumis, total_cumis, child_nums, parent_freq, child_to_parent, size_of_intvl = ([] for i in range(7))

	table = []

	f= open(file_name, "r")
	reader = csv.DictReader(f, delimiter='\t', fieldnames=headers)
	next(reader)
	counter = 0
	for row in reader:
		counter+=1

		#Build Sub-dataframe table
		str_cumi_lst = (row['CHILD_NUMS']).split(','); str_pumi_lst = (row['FREQ_PARENTS']).split(','); cumi_lst = []; pumi_lst = [];
		for i in str_cumi_lst:
			cumi_lst.append(int(i))
		for j in str_pumi_lst:
			pumi_lst.append(int(j))

		table.append(cumi_lst); table.append(pumi_lst)


		intvl_name = row['CHR']+":"+row['START']+"-"+row['END']
		region_len = str((int(row['END']))-(int(row['START'])))
		temp_intvl = row['CHR']+":"+row['START']+"+"+region_len
		c_to_p = (float(row['CTU']))/(float(row['PTU']))

		size_of_intvl.append(int(region_len)); child_to_parent.append(float(round(c_to_p,1))); region.append(temp_intvl); total_pumis.append(int(row['PTU'])); total_cumis.append(int(row['CTU'])); child_nums.append(row['CHILD_NUMS']); parent_freq.append(row['FREQ_PARENTS'])

	line = {'INTVL':region, 'PTU':total_pumis, 'CTU':total_cumis, 'CHILD_NUMS':child_nums, 'FREQ_PARENTS':parent_freq, 'INTVL_SIZE':size_of_intvl, 'CP':child_to_parent}
	df = pd.DataFrame(line, columns=df_headers)
	df.set_index('INTVL', inplace=True)

	headers_subdf=[]
	transp_table = [list(row) for row in itertools.zip_longest(*table, fillvalue=None)]
	col_nums = len(table)
	for i in range(1,col_nums+1):
		headers_subdf.append('col'+str(i))

	subframe = pd.DataFrame(transp_table, columns=headers_subdf)

	return df, subframe, name, col_nums, region

def plot_cp(df, output_path, name):
	#Plot Region vs. Child/Parent Ratio
	fig = plt.figure()
	df.sort_values('CP', ascending=False)['CP'].plot(kind='bar',x='INTVL',y='CP', color='pink', rot=90, title="Interval vs. Children to Parent Umis")
	plt.xlabel('Interval')
	plt.ylabel('Child:Parent Ratio')
	plt.tight_layout()
	plt.savefig(output_path+"CP_"+name+".png")
	plt.close(fig)

def plot_PTU(df, output_path, name):
	#Plot Region vs. Parent Umi Count
	fig = plt.figure()
	df.sort_values('PTU', ascending=False)['PTU'].plot(kind='bar',x='INTVL',y='PTU', color='red', rot=90, title="Interval vs. Parent Umi Count")
	#plt.gcf().subplots_adjust(bottom=0.15)
	plt.xlabel('Interval')
	plt.ylabel('Number of Parent UMIs')
	plt.tight_layout()
	plt.savefig(output_path+"PTU_"+name+".png")
	plt.close(fig)


def plot_CTU(df, output_path, name):
	#Plot Region vs. Child Umi Count
	fig = plt.figure()
	df.sort_values('CTU', ascending=False)['CTU'].plot(kind='bar',x='INTVL',y='CTU', color='blue', rot=90, title="Interval vs. Child Umi Count")
	plt.xlabel('Interval')
	plt.ylabel('Number of Child UMIs')
	plt.tight_layout()
	plt.savefig(output_path+"CTU_"+name+".png")
	plt.close(fig)

def plot_intvlsize_PTU_CTU(df, output_path, name):
	#Plot Interval size vs. Parent Umi Count & Child Umi Count
	ctu = df.plot(kind='scatter', x='INTVL_SIZE', y='CTU', color='blue', label="Child Umis Count")
	ptu = df.plot(kind='scatter', x='INTVL_SIZE', y='PTU', color = 'red', title="Interval Size vs. PTU and CTU", label="Parent Umi Count", ax=ctu)
	plt.legend()
	plt.tight_layout()
	plt.savefig(output_path+"CTU_PTU_intvlsize_"+name+".png")

def plot_child_pfreq(subframe, output_path, col_nums, regions):
	cnt = 0
	for i in range(0, col_nums, 2):
		#x_col = [subframe.columns[i]]
		#y_col = [subframe.columns[i+1]]

		subframe.plot(kind='scatter', x=i, y=i+1, color='purple', label="Parent Freq", title="No. of Children vs. Parent Freq.")
		plt.xlabel('Number of UMI Children')
		plt.ylabel('Frequency of Parents')

		plt.tight_layout()
		plt.savefig(output_path+"Children_vs_ParentFreq_"+str(regions[cnt])+".png")
		cnt+=1

def umi_plot(output_path, file_name, umi_flag):
	df, subframe, name, col_nums, regions = create_umi_dfs(file_name)

	if umi_flag == 'rs':
		plot_child_pfreq(subframe, output_path, col_nums, regions)
	elif umi_flag == 'all':
		plot_cp(df, output_path, name)
		plot_PTU(df, output_path, name)
		plot_CTU(df, output_path, name)
		plot_intvlsize_PTU_CTU(df, output_path, name)
		plot_child_pfreq(subframe, output_path, col_nums, regions)

		


#Consensus plots
def create_consdf(consfile):
	df_headers=['INTVL', 'CHROM', 'POS', 'REF', 'A', 'C', 'G', 'T', 'RAWDP', 'CONSDP', 'FAM', 'REF_FREQ', 'MEAN_FAM']
	df_headers2 = ['CHROM', 'POS', 'REF', 'A', 'C', 'G', 'T', 'RAWDP', 'CONSDP', 'FAM', 'REF_FREQ', 'MEAN_FAM']
	#df = pd.read_csv(consfile, sep='\t', columns=df_headers2)

	df = pd.read_csv(consfile, sep='\t')
	df.columns = ['CHROM', 'POS', 'REF', 'A', 'C', 'G', 'T', 'I', 'D', 'N', 'RAWDP', 'CONSDP', 'FAM', 'REF_FREQ', 'MEAN_FAM']
	return df

def plot_depth(df, output_path):
	figure(num=None, figsize=(15, 13), dpi=80, facecolor='w', edgecolor='k')
	groups=("zero","one", "two", "five")

	colors = ['blue', 'green', 'red', 'purple']
	ax = plt.scatter(x, y, c=label, cmap=matplotlib.colors.ListedColormap(colors))

	#plt.legend()
	plt.yscale('log')
	plt.xlim([min_pos, max_pos])
	plt.yticks([100, 1000, 10000, 100000, 1000000])

	plt.xticks(np.arange(min_pos, max_pos, step_pos))
	plt.ticklabel_format(useOffset=False, style='plain', axis='x')
	plt.xlabel = "Base Position"
	plt.ylabel = "Depth"

	plt.savefig(output_path+"base_pos_vs_CONSDP.png")


def plot_reffeq(df, output_path):

	figure(num=None, figsize=(15, 13), dpi=80, facecolor='w', edgecolor='k')

	groups=("zero","one", "two", "five")

	x = df['POS']
	y = df['REF_FREQ']
	label=df['FAM']

	colors = ['blue', 'green', 'red', 'purple']
	ax = plt.scatter(x, y, c=label, cmap=matplotlib.colors.ListedColormap(colors))

	#plt.legend(label, colors)

	min_pos = min(df['POS'])
	max_pos = max(df['POS'])
	step_pos = (max_pos-min_pos)/5

	min_reffreq = min(df['REF_FREQ'])
	max_reffreq = max(df['REF_FREQ'])
	step_reffreq = (max_reffreq-min_reffreq)/5

	plt.xlim([min_pos, max_pos])
	plt.yticks(np.arange(min_reffreq, max_reffreq, step_reffreq))

	plt.xticks(np.arange(min_pos, max_pos, step_pos))
	plt.ticklabel_format(useOffset=False, style='plain', axis='x')
	plt.xlabel = "Base Position"
	plt.ylabel = "Refrence Frequency"

	plt.savefig(output_path+"base_pos_vs_REFFREQ.png")






def cons_plot(output_path, file_name, cons_flag):

	if cons_flag == 'all':
		df = create_consdf(file_name)
		plot_depth(df, output_path)
		plot_reffeq(df, output_path)





