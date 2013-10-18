/*************************************************************************
* Copyright (C) 2013, Omar Andres Zapata Mesa                            *
* All rights reserved.                                                   *
*                                                                        *
* For the list of contributors see $ROOTSYS/README/CREDITS.              *
*************************************************************************/

#include<string>
#include<sstream>
#include<iostream>
#include<fstream>
#include<list>
#include"TStdIOHandler.h"

extern "C"
{
#include<string.h>  
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include<fcntl.h>
}
using namespace ROOT;

TStdIOHandler::TStdIOHandler()
{
  fCapturing=false;
}

void TStdIOHandler::InitCapture()
{
    if(!fCapturing)
    {
      /* save stdout/stderr for display later */
      SavedStdoutFd = dup(STDOUT_FILENO);  
      SavedStderrFd  = dup(STDERR_FILENO);  
      if( pipe2(StdoutPipeFd, O_NONBLOCK )  != 0 ) {          /* make a pipe for stdout*/
	 std::cerr<<"Error opening stdout \n";
         return;
      }
      if( pipe2(StderrPipeFd, O_NONBLOCK )  != 0 ) {          /* make a pipe for stdout*/
	std::cerr<<"Error opening stderr \n";
         return;
      }

      long flags = fcntl(StdoutPipeFd[0], F_GETFL); 
      flags |= O_NONBLOCK; 
      fcntl(StdoutPipeFd[0], F_SETFL, flags);
      
      flags = fcntl(StderrPipeFd[0], F_GETFL); 
      flags |= O_NONBLOCK; 
      fcntl(StderrPipeFd[0], F_SETFL, flags);
      
      dup2(StdoutPipeFd[1], STDOUT_FILENO);   /* redirect stdout to the pipe */
      close(StdoutPipeFd[1]);
      
      dup2(StderrPipeFd[1], STDERR_FILENO);   /* redirect stderr to the pipe */
      close(StderrPipeFd[1]);
      
      fCapturing = true;
    }
 }
  
void TStdIOHandler::EndCapture()
  {
    if(fCapturing)
    {
      fflush(stdout);
      fflush(stderr);
      int buf_readed;
      
      while(true)/* read from pipe into buffer */
      {
	buf_readed = read(StdoutPipeFd[0], fBuffer, MAX_LEN);
	if(buf_readed<=0) break;
	StdoutPipe += fBuffer;
	memset(fBuffer,0,MAX_LEN+1);
      }

      while(true)/* read from pipe into buffer */
      {
	buf_readed = read(StderrPipeFd[0], fBuffer, MAX_LEN);
	if(buf_readed<=0) break;
	StderrPipe += fBuffer;
	memset(fBuffer,0,MAX_LEN+1);
      }

      dup2(SavedStdoutFd, STDOUT_FILENO);  /* reconnect stdout*/
      dup2(SavedStderrFd, STDERR_FILENO);  /* reconnect stderr*/
      fCapturing = false;
    }
  }
  
std::string TStdIOHandler::GetStdout()
{
      return StdoutPipe;
}

std::string TStdIOHandler::GetStderr()
{
   return StderrPipe;
}

void TStdIOHandler::Clear()
{
    StdoutPipe="";
    StderrPipe="";
}
