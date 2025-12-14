
import {date as utilDate} from 'quasar'

export const MONTH_ARR = [
    {en: "January", bn: "জানুয়ারি"},
    {en: "February", bn: "ফেব্রুয়ারি"},
    {en: "March", bn: "মার্চ"},
    {en: "April", bn: "এপ্রিল"},
    {en: "May", bn: "মে"},
    {en: "June", bn: "জুন"},
    {en: "July", bn: "জুলাই"},
    {en: "August", bn: "আগষ্ট"},
    {en: "September", bn: "সেপ্টেম্বর"},
    {en: "October", bn: "অক্টোবর"},
    {en: "November", bn: "নভেম্বর"},
    {en: "December", bn: "ডিসেম্বর"}
];

export const WEEK_DAY_ARR = [
    {"en": "Sunday", "bn": "রবিবার "},
    {"en": "Monday", "bn": "সোমবার "},
    {"en": "Tuesday", "bn": "মঙ্গলবার "},
    {"en": "Wednesday", "bn": "বুধবার "},
    {"en": "Thursday", "bn": "বৃহস্পতিবার "},
    {"en": "Friday", "bn": "শুক্রবার"},
    {"en": "Saturday", "bn": "শনিবার "}
];

export const NUMBER_ARR = [
    {en: "0", bn: "০"},
    {en: "1", bn: "১"},
    {en: "2", bn: "২"},
    {en: "3", bn: "৩"},
    {en: "4", bn: "৪"},
    {en: "5", bn: "৫"},
    {en: "6", bn: "৬"},
    {en: "7", bn: "৭"},
    {en: "8", bn: "৮"},
    {en: "9", bn: "৯"}
]

export const PERIOD_ARR = [
    {en: "AM", bn: "পূর্বাহ্ণ "},
    {en: "PM", bn: "অপরাহ্ণ"}
]

export const  DMY =  {
    days : {en: 'days', bn: 'দিন'},
    yesterday: {en: 'yesterday', bn: 'গতকাল'},

    years: {en: 'years', bn: 'বছর'},
    year: {en: 'year', bn: 'বছর'},

    months: {en: 'months', bn: 'মাস'},
    month: {en: 'month', bn: 'মাস'},

    hours: {en: 'hours', bn: 'ঘন্টা'},
    hour: {en: 'hour', bn: 'ঘন্টা'},

    minutes: {en : 'minutes', bn: 'মিনিট'},
    minute: {en: 'minute', bn: 'মিনিট'},

    seconds: {en: 'seconds', bn: 'সেকেন্ড'},
    second: {en: 'second', bn: 'সেকেন্ড'},

    ago: { en: 'ago', bn: 'পূর্বে'},

}

const __ifNotDateInit = (isoUTC$) => {
    if(isoUTC$ instanceof Date == false)
        return new Date(isoUTC$)
    else return isoUTC$;
}

export const  fNumber = (number$, langCode$, padStart$) => {


    let numberTxt = number$ + '';
    let result = "";
    if(langCode$ == 'en')
        result = numberTxt;
    else
    {
        for (let i = 0; i < numberTxt.length; i++) {
            let char = numberTxt.charAt(i);
            result += NUMBER_ARR[char][langCode$];
        }
    }

    if(padStart$)
    {
        result = result.padStart(padStart$, NUMBER_ARR[0][langCode$])
        // debugger;
    }
    return result;
}

export const fMonth = (monthIdx$, langCode$) => {
    return MONTH_ARR[monthIdx$][langCode$];
}

export const fWeekDay = (dayIdx$, langCode$) => {
    return WEEK_DAY_ARR[dayIdx$][langCode$];
}

export const fDate = (dateObj$, langCode$) => {
    dateObj$ = __ifNotDateInit(dateObj$);
    let weekDay = WEEK_DAY_ARR[dateObj$.getDay()][langCode$];
    let month = MONTH_ARR[dateObj$.getMonth()][langCode$];
    let monthDay = fNumber(dateObj$.getDate(), langCode$);
    let year = fNumber(dateObj$.getFullYear(), langCode$);

    return `${weekDay}, ${month} ${monthDay}  ${year}`;
}

export const fShortDate = (dateObj$, langCode$) => {
    dateObj$ = __ifNotDateInit(dateObj$);
    //let weekDay = WEEK_DAY_ARR[dateObj$.getDay()][langCode$];
    let month = MONTH_ARR[dateObj$.getMonth()][langCode$];
    let monthDay = fNumber(dateObj$.getDate(), langCode$);
    // let year = fNumber(dateObj$.getFullYear(), langCode$);

    return `${monthDay} ${month}`;
}

export const fSimpleDate = (dateObj$, langCode$) => {
    dateObj$ = __ifNotDateInit(dateObj$);
    let month = MONTH_ARR[dateObj$.getMonth()][langCode$];
    let monthDay = fNumber(dateObj$.getDate(), langCode$);
    let year = fNumber(dateObj$.getFullYear(), langCode$);

    return `${month} ${monthDay} ${year}`;
}

export const fDateTime = (dateObj$, langCode$) => {
    dateObj$ = __ifNotDateInit(dateObj$);
    let lDate = fSimpleDate(dateObj$, langCode$);

    let lTime = fTime(dateObj$, langCode$);
    return lDate+' '+lTime;
}

export const fDaTimeObj = (dateObj$, langCode$) => {
    dateObj$ = __ifNotDateInit(dateObj$);
    //let lDate = fSimpleDate(dateObj$, langCode$);

    let weekDay = WEEK_DAY_ARR[dateObj$.getDay()][langCode$];
    let month = MONTH_ARR[dateObj$.getMonth()][langCode$];
    let monthDay = fNumber(dateObj$.getDate(), langCode$);

    let lDate = `${month} ${monthDay}`
    let lTime = fTime(dateObj$, langCode$);
    return {weekDay:weekDay, date: lDate, time: lTime};
}

export const fTime = (date$, langCode$) =>
{
    let tPeriod = 0; // am

    let tHour = date$.getHours();
    let tMin = date$.getMinutes();


    if(tHour < 12){
        tPeriod = 0;
        if(tHour == 0)
            tHour = 12;
    }
    else
    {
        tPeriod = 1; // pm
        if(tHour > 12)
            tHour = tHour - 12;
    }

    let hour = fNumber(tHour, langCode$);
    let min = fNumber(tMin, langCode$, 2);
    let hrPeriod = PERIOD_ARR[tPeriod][langCode$];

    return `${ hour }:${ min } ${hrPeriod} `;
}


export const fDiffMins = (utc$)=> {
    let daTime = __ifNotDateInit(utc$);
    let nowDaTime = new Date();
    return utilDate.getDateDiff(nowDaTime, daTime, 'minutes');
}

export const fAgoFromNow = (utc$, langCode$) => {

    let daTime = __ifNotDateInit(utc$);
    let nowDaTime = new Date();
    let i18Ago = DMY.ago[langCode$];
    let i18Diff = 0;

    let yearDiff = utilDate.getDateDiff(nowDaTime, daTime, 'years');
    i18Diff = fNumber(yearDiff, langCode$);
    if(yearDiff > 1)
        return `${i18Diff} ${DMY.years[langCode$]} ${i18Ago}`;
    if(yearDiff == 1)
        return `${i18Diff} ${DMY.year[langCode$]} ${i18Ago}`;



    let monthDiff = utilDate.getDateDiff(nowDaTime, daTime, 'months');
    i18Diff = fNumber(monthDiff, langCode$);
    if(monthDiff > 1)
        return `${i18Diff} ${DMY.months[langCode$]} ${i18Ago}`;
    if(monthDiff == 1)
        return `${i18Diff} ${DMY.month[langCode$]} ${i18Ago}`;


    let dayDiff = utilDate.getDateDiff(nowDaTime, daTime, 'days');
    i18Diff = fNumber(dayDiff, langCode$);
    if(dayDiff > 1)
        return `${i18Diff} ${DMY.days[langCode$]} ${i18Ago}`;
    if(dayDiff == 1)
        return `${DMY.yesterday[langCode$]}`;


    let hrDiff = utilDate.getDateDiff(nowDaTime, daTime, 'hours');
    i18Diff = fNumber(hrDiff, langCode$);
    if(hrDiff > 1)
        return `${i18Diff} ${DMY.hours[langCode$]} ${i18Ago}`;
    if(hrDiff == 1)
        return `${i18Diff} ${DMY.hour[langCode$]} ${i18Ago}`

    let minDiff = utilDate.getDateDiff(nowDaTime, daTime, 'minutes');
    i18Diff = fNumber(minDiff, langCode$);
    if(minDiff > 1)
        return `${i18Diff} ${DMY.minutes[langCode$]} ${i18Ago}`;
    if(minDiff == 1)
        return `${i18Diff} ${DMY.minute[langCode$]} ${i18Ago}`


    let secDiff = utilDate.getDateDiff(nowDaTime, daTime, 'seconds');
    i18Diff = fNumber(secDiff, langCode$);
    if(secDiff > 1)
        return `${i18Diff} ${DMY.seconds[langCode$]} ${i18Ago}`;
    if(secDiff == 1)
        return `${i18Diff} ${DMY.second[langCode$]} ${i18Ago}`

}

