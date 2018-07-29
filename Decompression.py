"""
    File : Unzip files downloaded from Google API page
 Authors : Minhoe Hur
  +Email : mhoe.hur@gmail.com
          
 History :
  2013/04/15 Minhoe Hur - Created
  2018/01/28 Minhoe Hur - Modified

   Notes :
  This program is runs under Python 3.x Runtime Environments.
"""
# -*- coding: utf-8 -*-

#import Download_config
import zipfile, glob, os, sys

def GetFileList( PATH, filetypeList ):
    print(' - Accessing to Path for loading filelist : %s' %PATH)
    fileList    =   []
    totcnt = 0
    if not os.path.isdir(PATH):
        print   (' Folder  \'%s\'  does not exist. ' %PATH )
        print   (' Please check your path.' )
        print
    else:
        for filetype in filetypeList:
            fileListTmp = glob.glob( os.path.join(PATH, '*.' + filetype) )
            aaa = [f.replace(PATH, '') for f in fileListTmp]
            fileList.extend(aaa)
            print(' - %s *.%s files are found in the directory and saved in the Filelist. ' %(len(aaa), filetype))
            totcnt = totcnt + len(aaa)
    print(' - Total %s files are found' %(totcnt))
    return fileList, totcnt

def Unzip( PATH, target_file, DestPATH ):
    zfile = zipfile.ZipFile(os.path.join(PATH, target_file),'r')
    print(' Extracting file ', '[', target_file, ']', '->',)
    for filename in zfile.namelist():
        try:
            print(filename  , )
            data = zfile.read(filename)
            decomp_file = open(os.path.join(DestPATH, filename), 'w+b')
            decomp_file.write(data)
            decomp_file.close()
        except:
            print(' Error in decompression of zip file', filename)
            
    print
#
# if __name__ == '__main__':
#     zipfile_list, totcnt = GetFileList(Download_config.LOCAL_ZIP, ['zip'])
#     cnt = 1
#
#     for target_file in zipfile_list:
#         print(' Extracting file ', ' [', cnt, '/', totcnt, ']')
#         Unzip(Download_config.LOCAL_ZIP, target_file, Download_config.LOCAL_BASE)
#         cnt = cnt + 1
#     print(' \n Program successfully terminated. ')
#