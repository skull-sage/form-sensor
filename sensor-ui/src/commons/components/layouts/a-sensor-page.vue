<template>
  <q-page v-mutation.childList="calcNavList">
    <slot></slot>
    <q-scroll-observer @scroll="trackScroll" :debounce="700" />
    <q-resize-observer @resize="calcNavList" :debounce="300" />
    <q-page-sticky expand position="top" ref="stickyTop">
      <b-container class="full-width   shadow-6 sticky-top bg-nav">
        <div class="q-mt-xs q-ml-xs text-teal-1  text-bold">{{title}}</div>
        <q-tabs align="left" class="text-teal-2" active-color="white"
          v-model="selected" @click="triggerScroll(selected)" >
          <q-tab :name="index"
                 :label="nav.label"
                 v-for="(nav, index) in  navList"
                 :key="index" />
        </q-tabs>
      </b-container>
    </q-page-sticky>
  </q-page>
</template>

<script>
  import {calcElmBox, calcScreenSize} from 'src/commons/utils/dom-util.js'

  let screenSize = calcScreenSize();

  export default {
    name: "a-sensor-page", // old:: multi-section-page
    props: ['title'],
    data(){
      return {
        topOffset : 0,
        selected: 0,
        navList : [],
      }
    },


    updated() {
      this.$nextTick(this.domUpdateHook);
    },

    methods:{

      trackScroll(scrollInfo$)
      {
        let position = Math.round(scrollInfo$.position + this.topOffset) + 1;
        let direction = scrollInfo$.direction; // "up, down"
/*
        if(this.navList.length == 0 || this.selected == undefined)
          return;
        let currentNav = this.navList[this.selected];
        if(currentNav.docTop + 100 >= position + screenSize.height)
          this.selected = undefined;
        else if(currentNav.docTop + currentNav.height - 100 <= position)
          this.selected = undefined;*/

        /*if(direction == 'up'){
         // selected => height <= 400px  : position is around ~10px of nav.docTop
                   //=> height > 400px: position is around nav.docTop +

       }
       */

        let start = position;
        let end = start + Math.round(screenSize.height/3); //33%


        if(direction == 'down')
        {

          for(let idx = 0; idx < this.navList.length; idx++){
            let nav = this.navList[idx];
            let crossSide = nav.docTop; // top side
            if(start <= crossSide && crossSide <= end){
              this.selected = idx;
              return;
            }
          }
        }
        else{
          // bottom side

          for(let idx = 0; idx < this.navList.length; idx++){
            let nav = this.navList[idx];
            let crossSide = nav.docTop + nav.height;
            if(crossSide >= end){
              this.selected = idx;
              return;
            }
          }

        }

      },

      triggerScroll(){

          let nav = this.navList[this.selected];



          window.scrollTo({
            top: nav.docTop - this.topOffset, // this is top in relation to document not viewport
            behavior: 'smooth'
          });
      },

      calcNavList( ){

        let _navList = [];
        let sectionList = this.$el.querySelectorAll('section');
        sectionList.forEach(section => {
          let sectionBox = calcElmBox(section);

          let data = {
            label : section.dataset.label,
            docTop : sectionBox.docTop,
            height: sectionBox.rectHeight
          }

         _navList.push(data);


        })

       // console.log("## src: "+JSON.stringify(src$));
       // console.log(JSON.stringify(_navList));
        this.navList = _navList;

       // this.triggerScroll();

      },

      domUpdateHook(){
        // 2px shift to mitigate the empty space
        let stickyTopBox = calcElmBox(this.$refs.stickyTop.$el);
        this.$el.style.paddingTop =  (stickyTopBox.offsetHeight -2 )+ "px";
        this.$refs.stickyTop.$el.style.marginTop = '-2px'
        this.topOffset = stickyTopBox.bottom;

      }
    }
  }
</script>

<style scoped lang="scss">
  .sticky-top {
    margin-top: -1px;
    border-top: 2px solid $blue-grey-1;

  }

  .top-nav{
     background-image: linear-gradient(to right, $amber-8, $amber-10);
  }
</style>
