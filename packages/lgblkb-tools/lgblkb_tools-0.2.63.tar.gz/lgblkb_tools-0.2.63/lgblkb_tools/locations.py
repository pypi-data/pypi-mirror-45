import shutil
from box import Box
import collections
import fnmatch
import glob
import os
import shutil
from datetime import datetime
from typing import Callable
import zipfile

get_name=lambda some_path:os.path.splitext(os.path.basename(some_path))[0]

def get_parent_dir(some_path,depth=1):
	for i in range(depth):
		some_path=os.path.dirname(os.path.abspath(some_path))
	return some_path

def create_path(*paths,stop_depth=0):
	path=os.path.join(*paths)
	os.makedirs(get_parent_dir(path,stop_depth),exist_ok=True)
	return path

def get_existing_path(paths,silent=False):
	for p in paths:
		if os.path.exists(p): return p
	if not silent:
		raise NotImplementedError('Could not find any existing path.')

def clear_folder(folder,remove_subdirs=True):
	for the_file in os.listdir(folder):
		file_path=os.path.join(folder,the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
			elif remove_subdirs and os.path.isdir(file_path): shutil.rmtree(file_path)
		except Exception as e:
			print(e)

def get_full_paths_from(parent_dir: str):
	for file in os.listdir(parent_dir):
		yield os.path.join(parent_dir,file)

def get_splitted(path):
	folders=[]
	while 1:
		path,folder=os.path.split(path)
		
		if folder!="":
			folders.append(folder)
		else:
			if path!="":
				folders.append(path)
			break
	folders.reverse()
	return folders

class InfoDict(collections.OrderedDict):
	
	def get_dir_path(self,*paths):
		return os.path.join(*self.get_portions(),*paths)
	
	# def create_file_path(self,ext,dir_depth=1):
	# 	return create_info_path(self,ext=ext,*self.get_portions(),dir_depth=dir_depth)
	
	def get_portions(self):
		portions=list()
		for k,v in self.items():
			if v: portions.append(f"{k}_{v}")
			else: portions.append(k)
		return portions
	
	def get_text(self,delim="__"):
		return delim.join(self.get_portions())
	
	def __str__(self):
		return self.get_text()

# class JsonPicklable(ABC):
#
# 	def to_json(self):
# 		return jsonpickle.encode(self)

class ZipError(Exception):
	pass

# base_name, format, root_dir=None, base_dir=None

def _make_zipfile(base_name,base_dir,root_dir=None,dry_run=0,logger=None):
	"""Create a zip file from all the files under 'base_dir'.

	The output zip file will be named 'base_name' + ".zip".  Returns the
	name of the output zip file.
	"""
	save_cwd=os.getcwd()
	if root_dir: os.chdir(root_dir)
	zip_filename=base_name+".zip"
	archive_dir=os.path.dirname(base_name)
	
	if archive_dir and not os.path.exists(archive_dir):
		if logger is not None:
			logger.debug("creating %s",archive_dir)
		if not dry_run:
			os.makedirs(archive_dir)
	
	if logger is not None:
		logger.debug("creating '%s' and adding '%s' to it",
		             zip_filename,base_dir)
	
	if not dry_run:
		with zipfile.ZipFile(zip_filename,"w",
		                     compression=zipfile.ZIP_DEFLATED) as zf:
			path=os.path.normpath(base_dir)
			if path!=os.curdir:
				zf.write(path,path)
				if logger is not None:
					logger.debug("adding '%s'",path)
			for dirpath,dirnames,filenames in os.walk(base_dir):
				for name in sorted(dirnames):
					path=os.path.normpath(os.path.join(dirpath,name))
					zf.write(path,path)
					if logger is not None:
						logger.debug("adding '%s'",path)
				for name in filenames:
					path=os.path.normpath(os.path.join(dirpath,name))
					if os.path.isfile(path):
						zf.write(path,path)
						if logger is not None:
							logger.debug("adding '%s'",path)
	os.chdir(save_cwd)
	return zip_filename

class Folder(object):
	
	def __init__(self,path='',pseudo=False,parent=None):
		if isinstance(path,self.__class__): path=path.path
		assert isinstance(pseudo,bool)
		if not pseudo:
			if not path: path=os.getcwd()
			elif not os.path.exists(path):
				assert os.path.splitext(os.path.split(path)[-1])[-1]=='',f"Please, use folder path as input. Provided path is: \n{path}"
				os.makedirs(path)
			elif not os.path.isdir(path):
				path=get_parent_dir(path,1)
		self.path=path
		self.pseudo=pseudo
		self.__parent=parent
	
	@property
	def name(self):
		return os.path.split(self.path)[-1]
	
	def get_filepath(self,*name_portions,ext='',delim='_',include_depth=None,datetime_loc_index=None,**name_kwargs):
		parts=list()
		if include_depth not in [0,None]:
			if type(include_depth) is Callable:
				parent_parts=include_depth(get_splitted(self.path))
			elif type(include_depth) is int:
				parent_parts=get_splitted(self.path)[-include_depth:]
			elif type(include_depth) in [tuple,list]:
				parent_parts=[get_splitted(self.path)[-x] for x in include_depth]
			else:
				raise NotImplementedError(f'include_depth={include_depth}')
			parts.extend(parent_parts)
		# if include_parents:
		# 	parent=self
		# 	root_parts=list()
		# 	while True:
		# 		print('parent',parent)
		# 		print(parent.child_parts)
		# 		if parent.child_parts:
		# 			root_parts.append(parent.child_parts)
		# 		if parent.is_root: break
		# 		parent=parent.parent
		# 	if root_parts: parts.extend([y for x in root_parts[::-1] for y in x])
		part_portions=delim.join([str(x) for x in name_portions])
		if part_portions: parts.append(part_portions)
		part_kwargs=InfoDict(name_kwargs).get_portions()
		if part_kwargs: parts.extend(part_kwargs)
		if datetime_loc_index is not None: parts.insert(datetime_loc_index,datetime.now().strftime("%Y%m%d-%H:%M:%S"))
		assert parts,'Nothing if provided to create filepath.'
		return os.path.join(self.path,delim.join(parts).replace(' ',delim)+ext)
	
	def _mkdir(self,child_dirpath):
		return create_path(self.path,child_dirpath)
	
	def create(self,*child_folders,**info_kwargs):
		parts=list()
		if child_folders: parts.extend(child_folders)
		if info_kwargs: parts.extend(InfoDict(info_kwargs).get_portions())
		assert parts,'Nothing is provided to create directory'
		child_dirpath='__'.join(map(str,parts))
		
		if self.pseudo: path=os.path.join(self.path,child_dirpath)
		else: path=self._mkdir(child_dirpath)
		return self.__class__(path,pseudo=self.pseudo,parent=self)
	
	def delete(self):
		if self.pseudo: raise OSError('Cannot delete when in "pseudo" mode.')
		shutil.rmtree(self.path)
	
	def clear(self):
		if self.pseudo: raise OSError('Cannot delete when in "pseudo" mode.')
		self.delete()
		create_path(self.path)
	
	def children(self,*paths):
		return glob.glob(os.path.join(self.path,*(paths or '*')))
	
	def zip(self,zip_filepath='',save_path_formatter=None):
		max_attempts=5
		if not zip_filepath:
			zipfile_basepath=os.path.join(get_parent_dir(self.path),self.name)
		elif zip_filepath[-4:]=='.zip':
			zipfile_basepath=zip_filepath[:-4]
		else:
			zipfile_basepath=zip_filepath
		
		if save_path_formatter is not None: zipfile_basepath=save_path_formatter(zipfile_basepath)
		for i in range(max_attempts):
			fullpath=_make_zipfile(base_name=zipfile_basepath,root_dir=get_parent_dir(self.path),base_dir=self.name)
			#shutil.make_archive(base_name=zipfile_basepath,format='zip',root_dir=get_parent_dir(self.path),base_dir=self.name)
			zip_obj=zipfile.ZipFile(fullpath)
			if not zip_obj.testzip():
				return fullpath
			else:
				os.remove(fullpath)
		raise ZipError(f'Could not zip {self.path} to {zipfile_basepath}.zip.')
	
	def unzip(self,zip_filepath,create_subdir=True):
		# if save_path_formatter is None: save_path_formatter=lambda x:x
		zip_path=[zip_filepath,
		          zip_filepath+'.zip',
		          self.get_filepath(zip_filepath),
		          self.get_filepath(zip_filepath,ext='.zip')]
		zip_path=get_existing_path(zip_path)
		assert not os.path.isdir(zip_path),f'The folder "{zip_filepath}" cannot be unzipped.'
		if create_subdir:
			zipfilename=get_name(zip_path)
			self.get_filepath(zipfilename)
			shutil.unpack_archive(zip_path,self.create(zipfilename).path,'zip')
		
		else:
			shutil.unpack_archive(zip_path,self.path,'zip')
		return self
	
	def glob_search(self,*patterns,recursive=True):
		return glob.glob(self.get_filepath(*patterns),recursive=recursive)
	
	def rename(self,new_name):
		new_path=os.path.join(get_parent_dir(self.path),new_name)
		os.rename(self.path,new_path)
		self.path=new_path
		return self
	
	def move(self,dst_path):
		shutil.move(self.path,self.__class__(dst_path).path)
		return self
	
	def parent(self,depth=1):
		return self.__class__(get_parent_dir(self.path,depth=depth),pseudo=self.pseudo)
	
	def __getitem__(self,item):
		if os.path.splitext(item)[-1]:
			return self.get_filepath(item)
		else:
			return self.create(item)
	
	def __setitem__(self,key,value):
		filename,ext=os.path.splitext(key)
		if isinstance(value,str): string_obj=value
		elif type(value) in [list,tuple]:
			string_obj='\n'.join(map(str,value))
		elif isinstance(value,dict):
			ext=ext or '.yaml'
			if ext in ['.yaml','.yml']:
				Box(value).to_yaml(filename=self.get_filepath(filename,ext=ext))
				return
			elif ext=='.json':
				Box(value).to_json(filename=self.get_filepath(filename,ext=ext))
				return
			else:
				string_obj='\n'.join(map(lambda kv:f"{kv[0]}: {kv[1]}",value.items()))
		
		else: string_obj=str(value)
		# def writer(filehandler):
		# 	for k,v in value.items():
		# 		filehandler.writelines([f"{k}: {v}"])
		
		with open(self.get_filepath(filename,ext=ext or '.txt'),'w') as fh:
			fh.write(str(string_obj))
	
	def __repr__(self):
		return f"{self.__class__.__name__}(r'{self.path}')"

# class RemoteFolder(Folder):
#
# 	def __init__(self,path=''):
# 		super().__init__(path='')
# 		self.path=path
#
# 	def create(self,*child_folders,**info_kwargs):
# 		return super().create(*child_folders,is_remote=True,**info_kwargs)
#
# 	def delete(self):
# 		raise NotImplementedError
#
# 	def children(self,*paths):
# 		raise NotImplementedError

get_neighbor_path=lambda curr_path,filename:os.path.join(get_parent_dir(curr_path),filename)

def get_paths_matching(target_dir,match: str):
	items=os.listdir(target_dir)
	outs=list()
	for item in items:
		if match in item: outs.append(os.path.join(target_dir,item))
	return outs

def replace_ext(fpath,out_extension):
	base_path,ext=os.path.splitext(fpath)
	return base_path+out_extension

def find_file(directory,pattern):
	for root,dirs,files in os.walk(directory):
		for basename in files:
			if fnmatch.fnmatch(basename,pattern):
				filename=os.path.join(root,basename)
				return filename

def main():
	# project_folder=Folder(__file__)
	# logs_folder=project_folder.create('log_files')
	# results_folder=project_folder.create('Results')
	
	pass

if __name__=='__main__':
	main()
