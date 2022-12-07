<main bind:this={main} class:header class:footer on:scroll={Scroll}>
    <slot {scroller}/>
  </main>
  
  <div class="slotHeader" class:hide={hideHeader && scroller.hide}>
    <slot name="header"/>
  </div>
  
  <div class="slotFooter" class:hide={hideFooter && scroller.hide}>
    <slot name="footer"/>
  </div>
  
  <script>
    import {createEventDispatcher} from "svelte";
    const dispatch = createEventDispatcher();
    let main;
    export let scroller = {
      scroll: 0,
      direction: true,
      delta: 0,
      hide: false,
      initialScroll: 0
    };
    export let header = false;
    export let headerHeight = 64;
    export let hideHeader = false;
    export let footer = false;
    export let footerHeight = 64;
    export let hideFooter = false;
    export let threshold = 64;
    const Scroll = e => {
      const scroll = e.target.scrollTop;
      
      scroller = {
        scroll,
        direction: scroll > scroller.scroll,
        delta: scroll - scroller.initialScroll,
        hide: scroll > threshold && scroller.hide
          ? scroll - scroller.initialScroll > -threshold
          : scroll - scroller.initialScroll > threshold,
        initialScroll: (scroll > scroller.scroll) != scroller.direction
          ? scroll
          : scroller.initialScroll
      };
      
      dispatch('scroller', scroller);
    };
    $: if(main) {
      main.style.setProperty('--header-height', headerHeight + 'px');
      main.style.setProperty('--footer-height', footerHeight + 'px');
    }
  </script>
  
  <style>
    main {
      height: 100%;
      overflow-y: auto;
    }
    main.header {
      padding-top: var(--header-height, 0px);
    }
    main.footer {
      padding-bottom: var(--footer-height, 0px);
    }
    .slotHeader {
      position: fixed;
      top: 0px;
      left: 0px;
      width: 100%;
      transition: all .2s ease-in-out;
    }
    .slotHeader.hide {
      transform: translateY(-100%);
    }
    .slotFooter {
      position: fixed;
      bottom: 0px;
      left: 0px;
      width: 100%;
      transition: all .2s ease-in-out;
    }
    .slotFooter.hide {
      transform: translateY(100%);
    }
  </style>