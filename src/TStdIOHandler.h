/*************************************************************************
 * Copyright (C) 2013,  Omar Andres Zapata Mesa                           *
 * All rights reserved.                                                   *
 *                                                                        *
 *                                                                        *
 * For the list of contributors see $ROOTSYS/README/CREDITS.              *
 *************************************************************************/

#ifndef ROOT_TStdIOHandler
#define ROOT_TStdIOHandler
#include<string>
#include<sstream>
#include<iostream>
#include<fstream>
#include <list>

#define MAX_LEN 40
namespace ROOT
{
  class TStdIOHandler
  {
  public:
    TStdIOHandler();
    void InitCapture();
    void EndCapture();
    
    std::string GetStdout();
    std::string GetStderr();
    
    void Clear();
    
  private:
    bool fCapturing;
    //this values are to capture stdout, stderr
    std::string    StdoutPipe;
    std::string    StderrPipe;
    char fBuffer[MAX_LEN];
    int StdoutPipeFd[2];
    int StderrPipeFd[2];
    int SavedStderrFd;
    int SavedStdoutFd;
  };
}
#endif
