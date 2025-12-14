import {QNotify} from '../../boot/q-notify';

const Data_fetch =
  {
    data(){
      return {
        reqTrying : {},
      }
    },
    methods:
      {
        initReq(name$){
          this.reqTrying[name$] = true;

        },

        reqSuccess(name$){
          let successMsg
          if( this.$options.reqMsg[name$])
             successMsg = this.$options.reqMsg[name$].success;

          if(successMsg)
            QNotify.positive(successMsg);

          delete this.reqTrying[name$];
        },

        reqFailed(name$)
        {
          let failMsg;
          if( this.$options.reqMsg[name$])
            failMsg = this.$options.reqMsg[name$].fail;

          if(failMsg)
            QNotify.negative(this.reqTrying[name$].fail);

          delete this.reqTrying[name$];
        }
      }
  }

export default Data_fetch;
