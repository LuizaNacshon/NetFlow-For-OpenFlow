'''
Created on Apr 26, 2014

@author: Luiza Nacshon
'''


import Testrouteplane
import CreateCSVfile
import ComputeFlowentriesMain,CreateSummarizedFile
import os,sys
import time
import computeGBC



#from signal import signal, alarm, SIGALRM
import timeit



linesarray=[]
runId=1

def func():
    
    serial = 0
    
    d_min=60
    d_max=70
    meu=0.2
    AggMethod=1
    GBC = 0.9 
    
    
    numberofremovedFp =0
    numberofnewinstalled = 0
    delete_installed_Fp_runtime = 0
    add_installed_Fp_runtime = 0
    potentialginiValue = 0
    sleepcounter = 0
    while not os.path.exists(os.getcwd() + "/mininet_signal.txt"):
        print "waiting for mininet"
        pass
    os.remove(os.getcwd() + "/mininet_signal.txt")
    time.sleep(180)
    with open(os.getcwd() + '/' +   "FinalResults/runid.txt") as my_file:
        
        for line in my_file:
            if(len(line)>0):
                linesarray.append(line) 
                runId = int(linesarray[0]) +1
    file = open(os.getcwd() + '/' +   "FinalResults/runid.txt","w")
    file.write(format(runId))
    file.close()
    GBCres, list_ofNERs= computeGBC.return_GBC(GBC)
    list_ofNERs_to_print = ('|').join(i for i in list_ofNERs)


    try:
        os.remove(os.getcwd() + '/' +   "NER/selectedrouters.txt")  
    except: 
        print ""
        
        
    print "NetFlow Enabled Routers selected by the Highest GBC"
    print "---------------------------------------------"
    for idx, l in enumerate(list_ofNERs):
        print "NER",idx,":    ","MAC-Address    ", l



    
    
    if(int(AggMethod)==1):
        Meth='max-max'
    elif(int(AggMethod)==2):
        Meth='max-min'
    elif(int(AggMethod)==3):
        Meth='min-min'
    if(int(Algo)==1):
        Alg='NER'
    elif(int(Algo)==2):
        Alg='Greedy'
    
    
    CreateCSVfile.getUserAlgo(Algo)
    
    

#     import Beetweeness_calculation
#     sumb=0
#     
#     get_beetweenece=Beetweeness_calculation.betweenness_centrality(list_ofNERs)
#     #print 'get_beetweenece',get_beetweenece
#     for b in get_beetweenece:
#         #print 'b',b
#         sumb=sumb+b

    start = timeit.default_timer()
    add_installed_Fp_runtime = Testrouteplane.get_userArgs(AggMethod,Algo,list_ofNERs,runId,serial,meu,alpha)
    numlinks = Testrouteplane.get_number_of_links()
    

    
    serial = serial +1
    
    end = timeit.default_timer()
    Algoruntime = end - start

    writecounter = 10
    writetimeout = 10
    checkcounter = 0
    checktimeout = 300


    while True:
        
        if(writecounter == writetimeout):
                 writecounter=0
                 (giniValue,totalfreeentries,totalusedentries,all_routers_cr)=ComputeFlowentriesMain.Compute_freeflowentries(runId,serial,Algo,AggMethod)
                 
                 

                     
                 CreateSummarizedFile.Add_totalGreedy(Algoruntime,runId,serial,Alg, Meth,numlinks,\
                giniValue,d_min,d_max,list_ofNERs_to_print,len(list_ofNERs),float(GBCres),totalfreeentries,totalusedentries,giniThreshold,\
                        potentialginiValue,Testrouteplane.routing.alpha, \
                        numberofremovedFp,numberofnewinstalled,delete_installed_Fp_runtime,\
                         add_installed_Fp_runtime)
                 serial = serial +1
        
                 #if(sleepcounter == 1):
                 #time.sleep(8)



                 
        if(checkcounter == checktimeout):  
                 checkcounter = 0
                 if(Alg=='Greedy'):
                     
                     #if(sleepcounter == 0):
                        #time.sleep(initialsleep)
                     #sleepcounter=1
                     if (len(all_routers_cr)>0):
		             numberofremovedFp =0
		             numberofnewinstalled = 0
		             delete_installed_Fp_runtime = 0
		             add_installed_Fp_runtime = 0
		             start = timeit.default_timer()
		             potentialginiValue = Testrouteplane.compute_potential_flow_assigment(all_routers_cr)
		             if(giniValue - potentialginiValue > giniThreshold): 
		                 #print "giniValue",giniValue
		                 #print "potentialginiValue",potentialginiValue
		                 
		                 numberofremovedFp,numberofnewinstalled,delete_installed_Fp_runtime,\
		                 add_installed_Fp_runtime = Testrouteplane.inbalance_rechange()
		             else:
		                 Testrouteplane.no_change()
		             end = timeit.default_timer()
		             Algoruntime = end - start

        checkcounter +=1
        writecounter+=1
        
if __name__ == '__main__':

    row =int(sys.argv[1]) 
    with open(os.getcwd() + '/' +   'NFOInputsFile.csv') as file:
        line = list(file)[row].strip('\n')
        args=line.split(',')
        
    
    Algo=int(args[0])
    giniThreshold = float(args[1])#0.0000001
    alpha = float(args[2])
    initialsleep = int(args[3])
          
    func()
  
