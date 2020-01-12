import calendar
import datetime



class GetMondayDate(object):

    def getAllDayList(self,year):
        cal = calendar.Calendar()
        alldaylist = []
        for month in list(range(1,13)):
            listday = []
            for day in cal.itermonthdays(year,month):
                if day != 0:
                    listday.append(day)
            alldaylist.append(listday)
        return alldaylist

    def getdaydate(self,year,alldaylist,zj):
        filterdate = []
        for month in list(range(1,13)):
            for day in alldaylist[month - 1]:
                date = datetime.date(year,month,day)
                if date.isoweekday() == zj:
                    if len(str(date.month)) == 1:
                        month1 = '0' + str(date.month)
                    else:
                        month1 = str(date.month)
                    if len(str(date.day)) == 1:
                        day = '0'+str(date.day)
                    else:
                        day = str(date.day)
                    tmpstr = str(date.year) + "-" + str(month1) + "-" + str(day)
                    filterdate.append(tmpstr)
        return filterdate


    def run(self,years):
        total_monday_date = []
        for year in range(2020,years):
            total_monday = self.getdaydate(year,self.getAllDayList(year),1)
            total_monday_date += total_monday
        return total_monday_date
