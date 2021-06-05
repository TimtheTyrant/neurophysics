import os, re, sys, matplotlib.pyplot as plt, numpy as np, pandas as pd
# from tkinter import filedialog, Tk
from glob import glob
from tkinter import Tk,filedialog
def get_all_trial_folders_not_archived(ic_suite_fn):
	os.chdir(ic_suite_fn)
	dir_lst=os.listdir()
	trial_folder_name_lst=[]
	for dir_run in dir_lst:
		# dir_run=dir_lst[0]
		trial_folder_name=dir_run
		#test if trial_folder_name is not a folder
		boo  = os.path.isdir(trial_folder_name)
		#test if trial_folder_name starts with ic
		boo &=trial_folder_name[:2]!='ic'
		#test if trial_folder_name contains archiv
		boo &=trial_folder_name.find('archiv')==-1
		#if not, append it to the trial_folder_name_lst
		if boo:
			trial_folder_name_lst.append(trial_folder_name)
	return trial_folder_name_lst

def find_files(filename, search_path):
	'''recursively search everywhere inside of search_path and return all files matching filename.'''
	result = []
	for root, dir, files in os.walk(search_path):
		if filename in files:
			result.append(os.path.join(root, filename))
	return result

def find_file(**kwargs):
	'''recursively search everywhere inside of search_path for filename.  Returns the first found.  This could be optimized with a greedy algorithm.'''
	return find_files(**kwargs)[0]

def search_for_file (currdir = os.getcwd()):
	'''use a widget dialog to selecting a file.  Increasing the default fontsize seems too involved for right now.'''
	root = Tk()
	# root.config(font=("Courier", 44))
	tempdir = filedialog.askopenfilename(parent=root,
										 initialdir=currdir,
										 title="Please select a file")#,
										 # filetypes = (("all files","*.*")))
	root.destroy()
	if len(tempdir) > 0:
		print ("File: %s" % tempdir)
	return tempdir

def get_all_files_matching_pattern(file,trgt):
	"""returns a list of files in same folder as file.
	all files in list end in the string trgt.
	Example, trgt='_unwrap.csv'.
	"""
	# get all .csv files in the working directory of ^that file
	folder_name = os.path.dirname(file)
	os.chdir(folder_name)
	retval = os.listdir()#!ls
	file_name_list = list(retval)
	# check each file if it ends in .csv before merging it

	def is_trgt(file_name,trgt):
		return file_name[-len(trgt):]==trgt
	# def is_csv(file_name):
	#     return file_name[-4:]=='_unwrap.csv'
	file_name_list = [os.path.abspath(f) for f in file_name_list if is_trgt(f,trgt)]
	return file_name_list