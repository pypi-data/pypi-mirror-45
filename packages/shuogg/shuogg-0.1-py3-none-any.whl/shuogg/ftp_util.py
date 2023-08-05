# windows/linux--py2/3 均支持
import paramiko
import os


class FTP():
    """
    例子: ftp = FTP('39.1.222.119', 'root', '123456')
          ftp.upload_one("C:\\mysql_test.py", "/home/FTP_download/mysql_test.py")
          ftp.download_one("/home/FTP_downloads/quicksort.py", "C:\\Users\\linshuo.UT\\Desktop\\quicksort1.py")

    """

    def __init__(self, hostaddr, username, password):
        super(FTP, self).__init__()
        self.__trans = paramiko.Transport((hostaddr, 22))
        self.__trans.connect(username=username, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(self.__trans)

    def __del__(self):
        self.__trans.close()

    def get_allfiles_in_localdir(self, localdir):
        """
        递归获取本地某文件夹下所有文件的完整路径
        :param localdir: 文件夹的路径
        :return:
        """
        allfiles = []
        files = os.listdir(localdir)
        for x in files:
            filename = os.path.join(localdir, x)
            if os.path.isdir(filename):
                allfiles.extend(self.get_allfiles_in_localdir(filename))
            else:
                allfiles.append(filename)
        return allfiles

    def upload_one(self, fromfile, tofile, callback=None):
        """
        上传一个文件
        :param fromfile: 上传文件的完整路径
        :param tofile: 放置文件的完整路径
        :parma callback: 回调(int, int)-->(so_far_size, total_size)
        :return:
        """
        self.sftp.put(localpath=fromfile, remotepath=tofile, callback=callback)
        (file_path, file_name) = os.path.split(fromfile)
        print(file_name, '上传完成!')

    def download_one(self, fromfile, tofile):
        """
        下载文件
        :param fromfile:
        :param tofile:
        :return:
        """
        self.sftp.get(localpath=tofile, remotepath=fromfile)
        (file_path, file_name) = os.path.split(tofile)
        print(file_name, '下载完成!')

    def upload_dir(self, localdir, remotedir):
        """
        上传localdir下所有文件包括子目录里, 但这些文件最后堆一起, 没有分文件夹放
        :param localdir:
        :param remotedir:
        :return:
        """
        if remotedir[-1] == '/':  # 去掉路径最后的'/', 如果有的话
            remotedir = remotedir[0:-1]
        allfiles = self.get_allfiles_in_localdir(localdir)
        for fullpath in allfiles:
            filename = os.path.split(fullpath)[-1]
            remote_fullpath = remotedir + '/' + filename
            print('传输成功:' + filename)
            self.upload_one(fullpath, remote_fullpath)

    def close(self):
        self.__trans.close()


if __name__ == '__main__':
    print('ftp_util')
