#!/usr/bin/env  python

import json;
import time;
import os;
import subprocess
import logging
import commands

special_pg = "postmaster"
PROBLEM_KEY_MAP = [];
class WatchDog():
	global PROBLEM_KEY_MAP
	level = logging.INFO
	cmd_list = [];
	def start(self,cmd,keywords):
		rst = os.popen(cmd)
		time.sleep(5);
		pre_pid = self.getPidFromKey(keywords);
		if(pre_pid != None and len(pre_pid) != 0):
                    if(PROBLEM_KEY_MAP.count(keywords) >= 1):
                        log_mess = cmd + '--->Find Problem,Restart Success!';
		        PROBLEM_KEY_MAP.remove(keywords);
                    else:
                        PROBLEM_KEY_MAP.append(keywords);
                        log_mess = cmd + '--->Start Success!'
		else:
                    log_mess = cmd + "--->Start Failed No Pid record!"
		print log_mess;
		self.level = logging.INFO;
		self.setlog(log_mess,self.level)

	def stop(self,key_word):
		cmd_str = "ps -ef | grep %s |grep -v grep | awk '{print $2}'" %key_word
		pro_number = os.popen(cmd_str).readlines()
		for i in pro_number :
			cmd = 'kill -9 ' + i
			print 'kill num=',i
			os.system(cmd)
		log_mess = key_word + '  Stop'
		self.level = logging.INFO;
		self.setlog(log_mess,self.level)

	def restart(self,cmd,key_word):
		self.stop(key_word)
		self.start(cmd,key_word)
		log_mess = key_word + '  Restart'
		self.level = logging.INFO;
		self.setlog(log_mess,self.level);

	def setlog(self,message,log_level):
		now = time.strftime("%Y-%m-%d,test")
		log_filename = "%s.log" % now
		log_format = '[%(levelname)s] [%(asctime)s] %(message)s'
		logging.basicConfig(filename=log_filename,format=log_format,datefmt='%Y-%m-%d %H:%M:%S %p',filemode='a',level=log_level)
		if(log_level == logging.INFO):
			logging.info(message)
		elif(log_level == logging.ERROR):
			logging.error(message);
        def getPidFromKey(self,key_word):
            key_word_second = None;
            if(len(key_word.split(',')) > 1):
                key_list = key_word.split(',')
                key_word_first = key_list[0];
                key_word_second = key_list[1];
            else:
                key_word_first = key_word;
            p1 = subprocess.Popen(['ps', 'aux'], stdout=subprocess.PIPE)
            if(key_word_second == None):
                p2 = subprocess.Popen(['grep', key_word], stdin=p1.stdout, stdout=subprocess.PIPE)
            else:
                p2 = subprocess.Popen(['grep', key_word_first], stdin=p1.stdout, stdout=subprocess.PIPE)
                p2 = subprocess.Popen(['grep', key_word_second], stdin=p2.stdout, stdout=subprocess.PIPE)
            p3 = subprocess.Popen(['grep', '-v', 'grep'], stdin=p2.stdout, stdout=subprocess.PIPE)
            p4 = subprocess.Popen(['grep','-v','vi'], stdin=p3.stdout, stdout=subprocess.PIPE)
            p5 = subprocess.Popen(['grep','-v','vim'], stdin=p4.stdout, stdout=subprocess.PIPE)
            p6 = subprocess.Popen(['grep','-v','tail'], stdin=p5.stdout, stdout=subprocess.PIPE)
            p7 = subprocess.Popen(['awk','{print $2}'], stdin=p6.stdout, stdout=subprocess.PIPE)
            pid = p7.stdout.read();
            if(len(pid) == 0):
                pid = None;
            return pid;
            
	def monitor_process(self,cmd_list):
		for cmd_dict in cmd_list:
                        key_word_second = None;
                        pid = None
			cmd = cmd_dict["cmd"];
			cmd_nospace = cmd.split(' ')[0];
			key_word = cmd_dict["keywords"];
			if(key_word == "postgresql,test"):
				key_word = special_pg;
                        pid = self.getPidFromKey(key_word);
			if(pid == None):
				self.start(cmd,key_word)
			elif len(pid) > 1:
				pass
	def run(self):
		while 1:
			self.monitor_process(self.cmd_list)
			time.sleep(5);

	def register(self,cmd,keywords):
		keyword_map = {"cmd":cmd,"keywords":keywords};
		self.cmd_list.append(keyword_map);



if __name__=="__main__":
	ss = WatchDog()
	
	ss.register("nohup ffmpeg -re -i udp://127.0.0.1:4011 -c copy -acodec aac -strict -2 -f flv -y rtmp://127.0.0.1:19350/zhongwen/E83633E0-3DBF-4677-A5CB-DAA25B694BA4 >/dev/null 2>&1 &","ffmpeg,E83633E0-3DBF-4677-A5CB-DAA25B694BA4")
	ss.register("nohup ffmpeg -re -i udp://127.0.0.1:4012 -c copy -acodec aac -strict -2 -f flv -y rtmp://127.0.0.1:19350/zhongwen/ACF6DF36-C470-4A91-AF48-4C00F195E74A >/dev/null 2>&1 &","ffmpeg,ACF6DF36-C470-4A91-AF48-4C00F195E74A")
	ss.register("nohup ffmpeg -re -i udp://127.0.0.1:4013 -c copy -acodec aac -strict -2 -f flv -y rtmp://127.0.0.1:19350/zhongwen/D9B601FA-C483-44D2-964B-6109E594451C >/dev/null 2>&1 &","ffmpeg,D9B601FA-C483-44D2-964B-6109E594451C")
	ss.register("nohup ffmpeg -re -i udp://127.0.0.1:4014 -c copy -acodec aac -strict -2 -f flv -y rtmp://127.0.0.1:19350/zhongwen/4507A40A-5130-4669-B6D9-C835155F0AFB >/dev/null 2>&1 &","ffmpeg,4507A40A-5130-4669-B6D9-C835155F0AFB")
	ss.register("nohup ffmpeg -re -i udp://127.0.0.1:4015 -c copy -acodec aac -strict -2 -f flv -y rtmp://127.0.0.1:19350/zhongwen/E4BFA5F8-BA9C-4BB3-8B5F-6B27F753B304 >/dev/null 2>&1 &","ffmpeg,E4BFA5F8-BA9C-4BB3-8B5F-6B27F753B304")
	ss.run();

        
	while 1:
		time.sleep(2)
