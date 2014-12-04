#!/usr/bin/env python
#########################################################
#Arafat NOUREDDINE
#2014/11/19
#Purpose : Test LimaDetector state
#########################################################
import os
import sys
import PyTango
import time
import datetime

proxy = ''
#------------------------------------------------------------------------------
# build exception
#------------------------------------------------------------------------------
class BuildError(Exception):
  pass

#------------------------------------------------------------------------------
def prepare(proxy):

    print '\nprepare\n--------------'
    #Display time when state is STANDBY (just before Prepare())
    timeBegin = datetime.datetime.now()
    print timeBegin.isoformat(), ' - ', proxy.state()

    proxy.Prepare()

    #Display time when state is RUNNING (just after prepare())
    timePrepare = datetime.datetime.now()
    print timePrepare.isoformat(), ' - ', proxy.state()

    #Loop while state is RUNNING (prepare in progress...)
    state = proxy.state()
    while (state==PyTango.DevState.RUNNING):
        state = proxy.state()
        if state == PyTango.DevState.STANDBY:
            break
        print '\r', '...',
        time.sleep(0)

    #Display time when state is STANDBY (just after prepare is finish)
    timeEnd = datetime.datetime.now()
    print '\n', timeEnd.isoformat(), ' - ', proxy.state()
    print '\nDuration = ', ((timeEnd-timePrepare).total_seconds()*1000),'(ms)'
    return


#------------------------------------------------------------------------------
def snap(proxy):

    print '\nsnap\n--------------'
    #Configure the device    

    #Display time when state is STANDBY (just before Snap())
    timeBegin = datetime.datetime.now()
    print timeBegin.isoformat(), ' - ', proxy.state()

    proxy.Snap()

    #Display time when state is RUNNING (just after Snap())
    timeSnap = datetime.datetime.now()
    print timeSnap.isoformat(), ' - ', proxy.state()

    #Loop while state is RUNNING (acquisition in progress...)
    state = proxy.state()
    while (state==PyTango.DevState.RUNNING):
        state = proxy.state()
        if state == PyTango.DevState.STANDBY:
            break
        print '\r', '...',
        time.sleep(0)

    #Display time when state is STANDBY (just after acquisition is finish)
    timeEnd = datetime.datetime.now()
    print '\n', timeEnd.isoformat(), ' - ', proxy.state()
    print '\nDuration = ', ((timeEnd-timeSnap).total_seconds()*1000),'(ms)'
    return
    #return proxy.image


#------------------------------------------------------------------------------
# Usage
#------------------------------------------------------------------------------
def usage():
  print "Usage: [python] test_limadetector.py <my/device/proxy> <exposureTime> <nbFrames> <fileGeneration> <nb_loops>"
  sys.exit(1)


#------------------------------------------------------------------------------
# run
#------------------------------------------------------------------------------
def run(proxy_name = 'arafat/lima_basler/basler.2', exposure_time = 100, nb_frames = 10, file_generation = True, nb_loops = 1):
    # print arguments
    print '\nProgram inputs :\n--------------'
    print 'proxy_name\t = ', proxy_name
    print 'exposure_time\t =  %s (ms)' %(exposure_time)
    print 'nb_frames\t = ', nb_frames
    print 'file_generation\t = ', file_generation
    print 'nb_loops\t = ', nb_loops
    proxy = PyTango.DeviceProxy(proxy_name)
    #Configure the device
    print '\nConfigure Device attributes :\n--------------'
    nb_frames = int(nb_frames)
    print 'write exposureTime'
    proxy.exposureTime = float(exposure_time)
    print 'write nbFrames'
    proxy.nbFrames = int(nb_frames)
    print 'write fileGeneration'
    proxy.fileGeneration = int(file_generation)
    nb_loops = int(nb_loops)
    print '\n'
    try:
        current_loop = 0
        while(current_loop<nb_loops):
            print '\n============================'
            print 'Loop : ', current_loop,
            print '\n============================'
            prepare(proxy)
            snap(proxy)
            current_loop=current_loop+1
            state = proxy.state()
            if (state!=PyTango.DevState.STANDBY):
                raise Exception('FAIL : Acquisition is end with state (%s)' %(state))
            print '\noutput :\n--------------'
            print 'currentFrame = ', proxy.currentFrame
            if proxy.currentFrame!=nb_frames:
                raise Exception('FAIL : Acquired frames (%s) is different from requested nb_frames (%s)'  % (proxy.currentFrame, nb_frames))
        print '\nProgram outputs :\n--------------'
        print '\nimage = '
        return proxy.image
    except Exception as err:
	   sys.stderr.write('--------------\nERROR :\n--------------\n%s\n' %err)

#------------------------------------------------------------------------------
# Main Entry point
#------------------------------------------------------------------------------
if __name__ == "__main__":
#    if len(sys.argv) < 4:
#        usage()
    print run(*sys.argv[1:])
