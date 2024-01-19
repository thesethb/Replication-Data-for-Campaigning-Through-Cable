*Appendix 3: Stata Code


******************************************************
* Name: Seth Benson                                               *
* Date: 23 Sep 2021                                                  *
* Purpose: Lesson 12 (OVB and Missing Data)         *
*******************************************************

 

**********************************
* Standard Stata Configuration *
**********************************

 

cls
clear all
set more off
cap log close




 

********************************
*          Load Data           *
********************************


import delimited "C:\Users\Seth Benson\Desktop\NewsTranscripts\house_appearances_fundraising.csv"




********************************
* Making Variables   *
********************************

describe

summarize

gen name_cycle = cand_name + string(year)
sort name_cycle date
by name_cycle: gen contribution_3Day = (contribution_receipt_amount[_n]+contribution_receipt_amount[_n+1]+contribution_receipt_amount[_n+2])/3
by name_cycle: gen contribution_Prev3Day = (contribution_receipt_amount[_n-1]+contribution_receipt_amount[_n-2]+contribution_receipt_amount[_n-3])/3

by name_cycle: gen instate_3Day = (instate_contributionamount[_n]+instate_contributionamount[_n+1]+instate_contributionamount[_n+2])/3
by name_cycle: gen instate_Prev3Day = (instate_contributionamount[_n-1]+instate_contributionamount[_n-2]+instate_contributionamount[_n-3])/3

by name_cycle: gen outstate_3Day = (outstate_contributionamount[_n]+outstate_contributionamount[_n+1]+outstate_contributionamount[_n+2])/3
by name_cycle: gen outstate_Prev3Day = (outstate_contributionamount[_n-1]+outstate_contributionamount[_n-2]+outstate_contributionamount[_n-3])/3

by name_cycle: gen searches_Prev3Day = (search_results[_n-1]+search_results[_n-2]+search_results[_n-3])/3



drop if missing(contribution_3Day)
drop if missing(contribution_Prev3Day)

gen pres_party = 1 if party_y == party_x
replace pres_party = -1 if party_y != party_x
gen approval_rate = (approving - disapproving) * pres_party

encode name_cycle, gen(name_cycle2)
encode date, gen(date2)

*Incumbents are sometimes listed with a status of 2 if they had previously won a special election
replace inc = 1 if inc > 1 







*********************************************************
****************Paper Regression Tables******************
*********************************************************


**********************TABLE 1***********************************
eststo clear

xtset name_cycle2 date2
xtreg contribution_receipt_amount appearance_count searches_Prev3Day contribution_Prev3Day approval_rate, fe
eststo

xtreg instate_contributionamount appearance_count searches_Prev3Day instate_Prev3Day approval_rate, fe
eststo

xtreg outstate_contributionamount appearance_count searches_Prev3Day outstate_Prev3Day approval_rate, fe
eststo

esttab, compress
esttab using "C:\ss368\log\test.rtf", se onecell replace





*Creating log'd variables
gen ln_Contribution_3Day = ln(contribution_3Day + 1)
gen ln_contribution = ln(contribution_receipt_amount + 1)
gen ln_contribution_Prev3Day = ln(contribution_Prev3Day + 1)
gen ln_instate3 = ln(instate_3Day + 1)
gen ln_prev_instate3 = ln(instate_Prev3Day + 1)
gen ln_outstate3 = ln(outstate_3Day + 1)
gen ln_prev_outstate3 = ln(outstate_Prev3Day + 1)


*********************************
**********TABLE A1****************
*********************************
eststo clear

xtset name_cycle2 date2
xtreg contribution_receipt_amount appearance_count searches_Prev3Day contribution_Prev3Day approval_rate, fe
eststo

*3Day Contribution
xtreg contribution_3Day appearance_count searches_Prev3Day contribution_Prev3Day approval_rate, fe
eststo

*logged regression
xtreg ln_Contribution_3Day appearance_count searches_Prev3Day ln_contribution_Prev3Day approval_rate, fe
eststo

esttab, compress
esttab using "C:\ss368\log\test.rtf", se onecell replace







******************************************
************TABLE 2***********************
******************************************

eststo clear

*Using just incumbents
xtset name_cycle2 date2
preserve
drop if inc == 0
xtreg contribution_receipt_amount appearance_count searches_Prev3Day contribution_Prev3Day approval_rate, fe
eststo

*Instate
xtreg instate_contributionamount appearance_count searches_Prev3Day instate_Prev3Day approval_rate, fe
eststo

*Outstate
xtreg outstate_contributionamount appearance_count searches_Prev3Day outstate_Prev3Day approval_rate, fe
eststo

restore
*Using just challengers
xtset name_cycle2 date2
preserve
drop if inc == 1

xtreg contribution_receipt_amount appearance_count searches_Prev3Day contribution_Prev3Day approval_rate, fe
eststo

xtreg instate_contributionamount appearance_count searches_Prev3Day instate_Prev3Day approval_rate, fe
eststo

xtreg outstate_contributionamount appearance_count searches_Prev3Day outstate_Prev3Day approval_rate, fe
eststo
esttab, compress
esttab using "C:\ss368\log\test.rtf", se onecell replace
restore




****************************************
************TABLE A2********************
****************************************
*Testing Primetime vs Non-Primetime

gen non_primetime = 0
replace non_primetime = 1 if appearance_count > 0 & primetime == 0
xtset name_cycle2 date2

eststo clear
xtreg contribution_receipt_amount primetime non_primetime searches_Prev3Day contribution_Prev3Day approval_rate, fe
eststo
xtreg instate_contributionamount primetime non_primetime searches_Prev3Day instate_Prev3Day approval_rate, fe
eststo
xtreg outstate_contributionamount primetime non_primetime searches_Prev3Day outstate_Prev3Day approval_rate, fe
eststo
esttab, compress
esttab using "C:\ss368\log\test.rtf", se onecell replace




*******************************************************************************
*************in vs out of election season (tables three and four)**************
*******************************************************************************


generate splitat = ustrpos(date,"-")

generate str1 year_of = ""
replace year_of = usubstr(date,1,splitat - 1)
destring year_of,  replace

generate str1 month_day = ""
replace month_day = usubstr(date,splitat + 1,.)

gen in_cycle = 1 if year_of == year & month_day >= "06-01"
replace in_cycle = 0 if in_cycle != 1

preserve
drop if in_cycle == 0
tab month_day




***Out of cycle incumbents vs in cycle incumbents (Table 3)
preserve
drop if in_cycle == 1 | inc == 0
xtset name_cycle2 date2
eststo clear
xtreg contribution_receipt_amount primetime non_primetime searches_Prev3Day contribution_Prev3Day approval_rate, fe
eststo
xtreg instate_contributionamount primetime non_primetime searches_Prev3Day instate_Prev3Day approval_rate, fe
eststo
xtreg outstate_contributionamount primetime non_primetime searches_Prev3Day outstate_Prev3Day approval_rate, fe
eststo

restore

preserve

drop if in_cycle == 0 | inc == 0
xtset name_cycle2 date2
xtreg contribution_receipt_amount primetime non_primetime searches_Prev3Day contribution_Prev3Day approval_rate, fe
eststo
xtreg instate_contributionamount primetime non_primetime searches_Prev3Day instate_Prev3Day approval_rate, fe
eststo
xtreg outstate_contributionamount primetime non_primetime searches_Prev3Day outstate_Prev3Day approval_rate, fe
eststo

restore

esttab, compress
esttab using "C:\Users\Seth Benson\Desktop\test.rtf", se onecell replace

***Out of cycle non-incumbents vs in cycle non-incumbents (Table 4)
preserve
drop if in_cycle == 1 | inc == 0
xtset name_cycle2 date2
eststo clear
xtreg contribution_receipt_amount primetime non_primetime searches_Prev3Day contribution_Prev3Day approval_rate, fe
eststo
xtreg instate_contributionamount primetime non_primetime searches_Prev3Day instate_Prev3Day approval_rate, fe
eststo
xtreg outstate_contributionamount primetime non_primetime searches_Prev3Day outstate_Prev3Day approval_rate, fe
eststo

restore

preserve

drop if in_cycle == 0 | inc == 0
xtset name_cycle2 date2
xtreg contribution_receipt_amount primetime non_primetime searches_Prev3Day contribution_Prev3Day approval_rate, fe
eststo
xtreg instate_contributionamount primetime non_primetime searches_Prev3Day instate_Prev3Day approval_rate, fe
eststo
xtreg outstate_contributionamount primetime non_primetime searches_Prev3Day outstate_Prev3Day approval_rate, fe
eststo

restore

esttab, compress
esttab using "C:\Users\Seth Benson\Desktop\test.rtf", se onecell replace


********************************************
******Doing it for each year: Figure 3******
********************************************
xtset name_cycle2 date2

preserve
drop if year != 2010
xtreg contribution_receipt_amount primetime non_primetime searches_Prev3Day contribution_Prev3Day, fe
estimates store y2010
restore

preserve
drop if year != 2012
xtreg contribution_receipt_amount primetime non_primetime searches_Prev3Day contribution_Prev3Day, fe
estimates store y2012
restore

preserve
drop if year != 2014
xtreg contribution_receipt_amount primetime non_primetime searches_Prev3Day contribution_Prev3Day, fe
estimates store y2014
restore

preserve
drop if year != 2016
xtreg contribution_receipt_amount primetime non_primetime searches_Prev3Day contribution_Prev3Day, fe
estimates store y2016
restore

preserve
drop if year != 2018
xtreg contribution_receipt_amount primetime non_primetime searches_Prev3Day contribution_Prev3Day, fe
estimates store y2018
restore

preserve
drop if year != 2020
xtreg contribution_receipt_amount primetime non_primetime searches_Prev3Day contribution_Prev3Day, fe
estimates store y2020
restore

label variable primetime "Primetime Appearances"
label variable non_primetime "Non-Primetime Appearances"
label variable searches_Prev3Day "Search Trends"
label variable contribution_Prev3Day "Lag of Past 3 Days Giving"
label variable approval_rate "Net Presidential Approval"

coefplot(y2010, label(2010) offset(.40) msymbol(D)) (y2012, label(2012) offset(.24) msymbol(T)) (y2014, label(2014) offset(.08) msymbol(S)) (y2016, label(2016) offset(-.08) msymbol(+) msize(large)) (y2018, label(2018) offset(-.24) msymbol(X)) (y2020, label(2020) offset(-.40) msymbol(O)), drop(_cons contribution_Prev3Day searches_Prev3Day) xline(1, lwidth(vthin)) omitted levels(95) graphregion(color(white)) bgcolor(white) coeflabels(, wrap(15))

*xscale(log range(.5 2)) omitted xline(1, lcolor(black) lwidth(thin) lpattern(dash)) xsize(5.5) ysize(3.8)
*searches_Prev3Day contribution_Prev3Day

******************************************************************
*********Differentiating by Network Table 5(mom's idea)***********
******************************************************************
gen cnn_non_primetime = 0
replace cnn_non_primetime = 1 if cnn > 0 & cnn_primetime == 0
gen fox_non_primetime = 0
replace fox_non_primetime = 1 if fox > 0 & fox_primetime == 0
gen msnbc_non_primetime = 0
replace msnbc_non_primetime = 1 if msnbc > 0 & msnbc_primetime == 0
xtset name_cycle2 date2


eststo clear
xtreg contribution_receipt_amount cnn_primetime cnn_non_primetime fox_primetime fox_non_primetime msnbc_primetime msnbc_non_primetime searches_Prev3Day contribution_Prev3Day approval_rate if party_x == "D", fe
eststo
xtreg instate_contributionamount cnn_primetime cnn_non_primetime fox_primetime fox_non_primetime msnbc_primetime msnbc_non_primetime searches_Prev3Day contribution_Prev3Day approval_rate if party_x == "D", fe
eststo
xtreg outstate_contributionamount cnn_primetime cnn_non_primetime fox_primetime fox_non_primetime msnbc_primetime msnbc_non_primetime searches_Prev3Day contribution_Prev3Day approval_rate if party_x == "D", fe
eststo
esttab, compress
esttab using "C:\ss368\log\dem.rtf", se onecell replace

eststo clear
xtreg contribution_receipt_amount cnn_primetime cnn_non_primetime fox_primetime fox_non_primetime msnbc_primetime msnbc_non_primetime searches_Prev3Day contribution_Prev3Day approval_rate if party_x == "R", fe
eststo
xtreg instate_contributionamount cnn_primetime cnn_non_primetime fox_primetime fox_non_primetime msnbc_primetime msnbc_non_primetime searches_Prev3Day contribution_Prev3Day approval_rate if party_x == "R", fe
eststo
xtreg outstate_contributionamount cnn_primetime cnn_non_primetime fox_primetime fox_non_primetime msnbc_primetime msnbc_non_primetime searches_Prev3Day contribution_Prev3Day approval_rate if party_x == "R", fe
eststo
esttab, compress
esttab using "C:\ss368\log\rep.rtf", se onecell replace


