

import {Cookies} from 'quasar';
import {fDate, fTime, fDateTime, fNumber, fMonth, fDaTimeObj, fSimpleDate, fShortDate} from "../utils/lang-util";


const _langCode = Cookies.get('lang-code') || 'en';



export default {

  /**
   * langCode : defined in component local context || cookie || default 'en'
   * cLabel: component context label messages.
   * the transformation of cLabel is done in vue created hook for now,
   * might be moved to beforeUpdate lifecycle as per new features.
   *
   * */
  created()
  {

    //this.compLabel = Object.freeze(this.$options.compLabel);
    //this.langCode = this.cLangCode || this.$options.cLangCode ||  _langCode;
    let _cLabel = {...this.$options.cLabel};
    for(let key in _cLabel)
        _cLabel[key] = this.$l(_cLabel[key]);
    this.cLabel = Object.freeze(_cLabel);

  },


  computed: {
    cLangCode(){
      return this.langCode || this.$options.cLangCode || this.$options.langCode ||  _langCode;
    },
    langClass(){
      return 'lang-'+this.cLangCode
    }
  },

  methods:{


    $l(data$) // @deprecated
    {

      return this.$lData(data$);

    },

    $lNumber(number$){
      return fNumber(number$, this.cLangCode)
    },

    $lMonth(monthIdx$){
      return fMonth(monthIdx$, this.cLangCode);
    },


    $lDate(date$){


      return fDate(date$, this.cLangCode);
    },

    $lTime(date$){
      return fTime(date$, this.cLangCode);
    },

    $lDateTime(date$)
    {
      return fDateTime(date$, this.cLangCode);
    },

    $lDaTimeObj(isoStr$){
      return fDaTimeObj(isoStr$, this.cLangCode)
    },

    $lShortDate(isoStr$){
       return fShortDate(isoStr$, this.cLangCode)
    },


    $lData(data$){

      if(data$ instanceof Object)
        return data$[this.cLangCode];
      else data$;

    },

  },

}
