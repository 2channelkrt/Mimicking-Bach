import collections # this code is based on python 3.5, thus dictionary doesn't remember insertion orders
class csvFile:
    
    beatLib=[]
    
    def __init__(self, fileName):
        self.mData ={}
        self.mData['fileName']=fileName
        self.getMetaData()
        self.right={}
        self.left={}
    
    def convert2InputFormat(self):
        f=open(self.mData['fileName'],"r")
        content=f.read().splitlines()
        ##locate start of tarck 1
        i=0
        while(True):
            if(content[i].split(', ')[2]=='Start_track' and content[i+1].split(', ')[3]=='"Track 1"'):
                i+=1
                break
            i+=1
        ##now i has start of track 1
        while(True):
            line=content[i].split(', ')
            if(line[2]=='End_track'):
                curTrack=int(line[0])
                break
            if(line[2]=='Note_on_c'):
                self.InsertDic(self.right,line[1],line[4])
            i+=1
        self.right=collections.OrderedDict(sorted(self.right.items()))
        ##right created
        for trackNum in range(curTrack,int(self.mData['numTrack'])):
            while(True):
                if(content[i].split(', ')[2]=='Start_track'):
                    i+=1
                    break;
                i+=1
            ##now i has start of next track
            while(True):
                line=content[i].split(', ')
                if(line[2]=='End_track'):
                    curTrack=line[0]
                    break
                if(line[2]=='Note_on_c'):
                    self.InsertDic(self.left,int(line[1]),int(line[4]))
                i+=1
        f.close()
        self.left=dict(sorted(self.left.items()))

    def convert2OutputFormat(self, outPath):
        PathHeader=r"\\"
        newFileName=outPath+PathHeader+self.mData['fileName'][:-4]+'_converted'+self.mData['fileName'][-4:]
        f=open(newFileName,"w")
        self.findMaxTrackNum()
        f.write('0, 0, Header, 1, '+str(2)+', '+self.mData['division']+'\n')
        f.write('1, 0, Start_track\n')
        f.write('1, 0, Time_signature, 4, 2, 24, 8\n')
        f.write('1, 0, Tempo, '+self.mData['Tempo']+'\n')
        f.write('1, 0, SMPTE_offset, 64, 0, 0, 0, 100\n')
        f.write('1, 0, End_track\n')
        ##f.write('2, 0, Start_track\n')
        ##f.write('2, 0, Title_t, "Track 1"\n')
        ##f.write('2, 0, Program_c, 0, 6\n') # 6 specifies instrument type?

        curHardTrackNum=2
        ##write right hand
        print(self.mData['requireTrackR'])
        print(self.mData['requireTrackL'])
        for i in range(0,1):
            print("writing right track"+str(i))
            self.writeTrack(f,str(curHardTrackNum),str(i),self.right)
            curHardTrackNum+=1
        ##write left hand
        #for i in range(0,self.mData['requireTrackL']):
        #    print("writing left track"+str(i))
        #    self.writeTrack(f,str(curHardTrackNum),str(i),self.left)
        #    curHardTrackNum+=1

        f.write('0, 0, End_of_file')

        f.close()

    def findMaxTrackNum(self):
        maxIndex=0
        for key, val in self.right.items():
            if(len(val)>maxIndex):
                maxIndex=len(val)
        self.mData['requireTrackR']=maxIndex
        
        maxIndex=0
        for key, val in self.left.items():
            if(len(val)>maxIndex):
                maxIndex=len(val)
        self.mData['requireTrackL']=maxIndex

    def writeTrack(self, f, hardtrackNum, softTrackNum, source):##int values are sent as str
        fresh=True
        last_pitch=''
        last_timeStamp=''
        f.write(hardtrackNum+', 0, Start_track\n')
        f.write(hardtrackNum+', 0, Title_t, "Track '+str(int(hardtrackNum)-1)+'"\n')
        f.write(hardtrackNum+', 0, Program_c, '+str(int(hardtrackNum)-2)+', 6\n') # 6 specifies instrument type?
        for key, val in source.items():
            if(len(val)>int(softTrackNum)):##only if val has current track key to play
                if(fresh==False):
                    f.write(hardtrackNum+', '+str(int(key)-1)+', Note_off_c, '+str(int(hardtrackNum)-2)+', '+last_pitch+', 0\n')
                else:
                    fresh=False
                last_pitch=str(val[int(softTrackNum)])
                f.write(hardtrackNum+', '+str(key)+', Note_on_c, '+str(int(hardtrackNum)-2)+', '+str(val[int(softTrackNum)])+', 88\n')
                last_timeStamp=str(key)
        f.write(hardtrackNum+', '+str(int(last_timeStamp)+40)+', Note_off_c, '+str(int(hardtrackNum)-2)+', '+last_pitch+', 0\n')
        f.write(hardtrackNum+', '+str(int(last_timeStamp)+40)+', End_track\n')


    def getMetaData(self):
        f=open(self.mData['fileName'],"r")
        content=f.read().splitlines()[:5]
        self.mData['numTrack']=content[0].split(', ')[4]
        self.mData['division']=content[0].split(', ')[5]
        self.mData['Tempo']=content[3].split(', ')[3]

        f.close()

    def printInfo(self):
        for data in self.mData:
            print(""+data+": "+self.mData[data])

    def InsertDic(self, dic, key, val):
        key=int(key)
        val=int(val)
        if(key in dic):
            dic[key].append(val)
        else:
            dic[key]=[val]
    def getBasicTimeStep(self):
        if(len(self.right)==0):
            print("self.right track is empty. run .convert2InputFormat(self) first")
            return None
        
        prevKey=None
        minTimeStep=None
        timeStepLib={}
        for key, _ in self.right.items():
            if(prevKey==None):
                prevKey=key
                continue
            curTimeStep=key-prevKey
            if not curTimeStep in self.beatLib:
                self.beatLib.append(curTimeStep)
            if(curTimeStep in timeStepLib):
                timeStepLib[curTimeStep]+=1
            else:
                timeStepLib[curTimeStep]=1
            if(minTimeStep==None):
                minTimeStep=curTimeStep
                continue
            if(curTimeStep<minTimeStep):
                minTimeStep=curTimeStep
            prevKey=key
        self.mData['minTimeStep']=minTimeStep
        maxKey,maxVal=None, None
        for key, val in timeStepLib.items():
            if(maxKey==None):
                maxKey, maxVal=key, val
                continue
            if(val>maxVal):
                maxKey, maxVal=key, val
        self.mData['baseTimeStep']=maxKey
    def createInputData1(self): #declare dic here, since it may be deprecated
        self.inputData=[]
        pKey, pVal=None, None
        for key, val in self.right.items():
            if(pKey==None):
                pKey, pVal=key, val
                continue
            self.inputData.append([key-pKey,pVal[0]])#intentionally discarding last note
            pKey, pVal=key, val
            
            

##record note hit
##file will have to automatically generate note release

##read and record track 1 for right hand.
##read and record track 2~ for left hand. concat in dics.

##right hand, note auto release is not hard
##left hand, if next note is played, release all beforehand.

##for timestamp, 일정한 템포로 근사시킨다. RNN에 넣으려면 시간을 데이터로 넣지 말고 시퀸스로 넣어야 한다.