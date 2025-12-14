import {QNotify} from 'src/boot/q-notify';

const Data_fetch =
{
   data(){
     return {
       reqTrying : false,
       nReqTrying: {}
     }
   },
   methods:
    {
      nInitReq(name$){
        this.$set(this.nReqTrying, name$, true)

          return {
            success : (msg$)=>{
              this.$delete(this.nReqTrying, name$);
              if(msg$)
                QNotify.positive(msg$);
            },
            failed: (msg$)=>{
              this.$delete(this.nReqTrying, name$);
              if(msg$)
                QNotify.negative(msg$);
            }
          }

      },

      initReq(){

            this.reqTrying = true;
      },

      reqSuccess(msg$){
        this.reqTrying = false;
        if(msg$)
          QNotify.positive(msg$);
      },

      reqFailed(msg$)
      {
        this.reqTrying = false;
        if(msg$)
          QNotify.negative(msg$);

      }
    }
}

export default Data_fetch;
