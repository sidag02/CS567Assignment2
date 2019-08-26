import time
class Applicant:
    def __init__(self,t):
        self.applicantID=t[0:5]
        self.gender=t[5]
        self.age=int(t[6:9])
        self.pets = False
        if t[9] == 'Y':
            self.pets = True
        self.medicalCondition=False
        if t[10] == 'Y':
            self.medicalCondition = True
        self.car=False
        if t[11] == 'Y':
            self.car=True
        self.driverLicense=False
        if t[12] == 'Y':
            self.driverLicense=True
        #self.days={'M':0,'T':0,'W':0,'Th':0,'F':0,'S':0,'Su':0}
        self.days=[0]*7
        self.countOfDays=0
        if t[13] == '1':
            self.days[0]=1
            self.countOfDays+=1
        if t[14] == '1':
            self.days[1]=1
            self.countOfDays += 1
        if t[15] == '1':
            self.days[2]=1
            self.countOfDays += 1
        if t[16] == '1':
            self.days[3]=1
            self.countOfDays += 1
        if t[17] == '1':
            self.days[4]=1
            self.countOfDays += 1
        if t[18] == '1':
            self.days[5]=1
            self.countOfDays += 1
        if t[19] == '1':
            self.days[6]=1
            self.countOfDays += 1
        self.selectedByParking=False
        self.selectedByHousing=False
        self.eligibleForParking=False
        self.eligibleForHousing=False
        if self.age > 17 and self.gender == 'F' and not self.pets:
            self.eligibleForHousing = True
        if self.car and self.driverLicense and not self.medicalCondition:
            self.eligibleForParking = True
    def __lt__(self,other):
        return self.countOfDays>other.countOfDays
def isCompatible(applicant,dictionary):
    for day in range(7):
        if dictionary[day]-applicant.days[day]<0:
            return False
    return True
def optimize(availibilityList,applicantList):
    if time.time()-startTime>cutOff:
        return 0,0
    max=0
    id=''
    n=len(applicantList)
    if n==0:
        return max,id
    for i in range(n):
        if time.time()-startTime>cutOff:
            break
        if isCompatible(applicantList[i],availibilityList):
            applicant=applicantList[i]
            applicantList.remove(applicant)
            if len(applicantList)>0:
                for day in range(7):
                    availibilityList[day] -= applicant.days[day]
                key = ''
                x = 0
                y = 0
                for j in range(len(applicantList)):
                    key+=applicantList[j].applicantID
                for k in range(6):
                    key+=str(availibilityList[k])
                if key in optimalDictionary2:
                    x,y=optimalDictionary2[key]
                else:
                    x,y=optimize(availibilityList,applicantList)
                    optimalDictionary2[key]=(x,y)
                if x+applicant.countOfDays>max:
                    max=x+applicant.countOfDays
                    id=applicant.applicantID
                applicantList.append(applicant)
                for day in range(7):
                    availibilityList[day] += applicant.days[day]
            else:
                applicantList.append(applicant)
                return applicant.countOfDays,applicant.applicantID
        else:
            continue
    return max,id
def nextMove(maxSpla,maxHousing,applicantList,parkingDictionary,housingDictionary,isSplaTurn):
    if time.time()-startTime>cutOff:
        return 0,0,''
    maxS = maxSpla
    maxH = maxHousing
    maxId=""
    n = len(applicantList)
    canPlay=False
    if n == 0:
        key=''
        x=0
        y=0
        z=''
        id=''
        for applicant in parkingEligibleCandidates:
            key+=applicant.applicantID
        for day in parkingDictionary:
            key+=str(day)
        if key in optimalDictionary:
            x,id=optimalDictionary[key]
        else:
            x, id = optimize(parkingDictionary, parkingEligibleCandidates)
            optimalDictionary[key]=(x,id)
        key = ''
        for applicant in housingEligibleCandidates:
            key += applicant.applicantID
        for day in housingDictionary:
            key += str(day)
        if key in optimalDictionary:
            y, z = optimalDictionary[key]
        else:
            y, z = optimize(housingDictionary, housingEligibleCandidates)
            optimalDictionary[key]=(y,z)
        return x, y, id
    if isSplaTurn:
        for i in range(n):
            if time.time()-startTime>cutOff:
                break
            if isCompatible(applicantList[i],parkingDictionary):
                applicant=applicantList[i]
                applicantList.remove(applicantList[i])
                canPlay=True
                for day in range(7):
                    parkingDictionary[day] -= applicant.days[day]
                x,y,id=nextMove(maxSpla,maxHousing,applicantList,parkingDictionary,housingDictionary,False)
                if x+applicant.countOfDays>maxS:
                    maxS=x+applicant.countOfDays
                    maxH=y
                    maxId=applicant.applicantID
                applicantList.insert(i,applicant)
                for day in range(7):
                    parkingDictionary[day]+=applicant.days[day]
            else:
                continue
        key = ''
        x=0
        id=''
        if not canPlay:
            maxH,z=optimize(housingDictionary,housingEligibleCandidates+applicantList)
        for applicant in parkingEligibleCandidates:
            key += applicant.applicantID
        for day in parkingDictionary:
            key += str(day)
        if key in optimalDictionary:
            x, id = optimalDictionary[key]
        else:
            x, id = optimize(parkingDictionary, parkingEligibleCandidates)
            optimalDictionary[key] = (x, id)
        if x>maxS:
            maxS=x
            maxH,z=optimize(housingDictionary,housingEligibleCandidates+applicantList)
            maxId=id
        return maxS,maxH,maxId
    else:
        for i in range(n):
            if time.time()-startTime>cutOff:
                break
            if isCompatible(applicantList[i], housingDictionary):
                applicant=applicantList[i]
                canPlay=True
                applicantList.remove(applicantList[i])
                for day in range(7):
                    housingDictionary[day] -= applicant.days[day]
                x, y, id = nextMove(maxSpla, maxHousing, applicantList,parkingDictionary,housingDictionary, True)
                if y + applicant.countOfDays > maxH:
                    maxH = y + applicant.countOfDays
                    maxS = x
                    maxId = applicant.applicantID
                applicantList.insert(i,applicant)
                for day in range(7):
                    housingDictionary[day] += applicantList[i].days[day]
            else:
                continue
        key = ''
        y=0
        id=''
        if not canPlay:
            maxS,z=optimize(parkingDictionary,parkingEligibleCandidates+applicantList)
        for applicant in housingEligibleCandidates:
            key += applicant.applicantID
        for day in housingDictionary:
            key += str(day)
        if key in optimalDictionary:
            y, id = optimalDictionary[key]
        else:
            y, id = optimize(housingDictionary, housingEligibleCandidates)
            optimalDictionary[key]=(y,id)
        if y > maxH:
            maxH = y
            maxS, z = optimize(housingDictionary, parkingEligibleCandidates + applicantList)
            maxId = id
        return maxS, maxH, maxId

output=open("output.txt",'w')
startTime=time.time()
cutOff=170
input=open('input24.txt','r')

numberOfBeds=int(input.readline())
countOfBeds=numberOfBeds*7
housingDictionary=[numberOfBeds]*7
numberOfParkingSpots=int(input.readline())
countOfParkingSpots=numberOfParkingSpots*7
parkingDictionary=[numberOfParkingSpots]*7
applicantsChosenByHousing=int(input.readline())
applicantsChosenByHousingList=[]
parkingEligibleCandidates=[]
housingEligibleCandidates=[]
commonCandidates=[]
for i in range(0,applicantsChosenByHousing):
    applicantsChosenByHousingList.append(input.readline().strip('\r\n'))
applicantsChosenByParking=int(input.readline())
applicantsChosenByParkingList=[]
for i in range(0,applicantsChosenByParking):
    applicantsChosenByParkingList.append(input.readline().strip('\r\n'))
totalApplicants=int(input.readline())
applicantList=[]
for i in range(0,totalApplicants):
    t=input.readline().strip('\r\n')
    temp=Applicant(t)
    if temp.age>17 and temp.gender=='F' and not temp.pets:
        temp.eligibleForHousing=True
    if temp.car and temp.driverLicense and not temp.medicalCondition:
        temp.eligibleForParking=True
    if temp.applicantID in applicantsChosenByHousingList:
        temp.selectedByHousing=True
        for i in range(7):
            housingDictionary[i]-=temp.days[i]
            countOfBeds-=temp.days[i]
    if temp.applicantID in applicantsChosenByParkingList:
        temp.selectedByParking=True
        for i in range(7):
            parkingDictionary[i]-=temp.days[i]
            countOfParkingSpots-=temp.days[i]
    if (temp.eligibleForParking and temp.eligibleForHousing) and (not temp.selectedByHousing) and (not temp.selectedByParking):
        commonCandidates.append(temp)
    elif (temp.eligibleForParking and not temp.eligibleForHousing) and (not temp.selectedByHousing) and (not temp.selectedByParking):
        parkingEligibleCandidates.append(temp)
    elif(not temp.eligibleForParking and temp.eligibleForHousing) and (not temp.selectedByHousing) and (not temp.selectedByParking):
        housingEligibleCandidates.append(temp)
    else:
        continue

optimalDictionary={}
optimalDictionary2={}
parkingMax,housingMax,maxId=nextMove(0,0,commonCandidates,parkingDictionary,housingDictionary,True)
print maxId
output.write(maxId)
