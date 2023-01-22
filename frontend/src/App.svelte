<script>
  import Layout from "./lib/Layout.svelte";
	//import { Tabs, TabItem } from 'flowbite-svelte'; // TODO test if working 

  var url_str = "";
  var text_output = "";
  var video_id_str = "";
  var active = false;
  var spam_comments = ["Nice song!", "Love it", "Come on.. visit my page!"];

  var dashboard_src = "http://localhost:5601/app/dashboards#/view/3482a810-98f9-11ed-8c04-a96741ae86bb?embed=true&_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:'2023-01-14T06:43:19.849Z',to:now))&_a=(description:'',filters:!(),fullScreenMode:!f,options:(hidePanelTitles:!f,syncColors:!f,useMargins:!t),panels:!((embeddableConfig:(attributes:(references:!((id:d9c60ca0-98f8-11ed-8c04-a96741ae86bb,name:indexpattern-datasource-current-indexpattern,type:index-pattern),(id:d9c60ca0-98f8-11ed-8c04-a96741ae86bb,name:indexpattern-datasource-layer-57bae6dc-841f-49e9-85a4-c44b568d8400,type:index-pattern)),state:(datasourceStates:(indexpattern:(layers:('57bae6dc-841f-49e9-85a4-c44b568d8400':(columnOrder:!('0b5a3122-8fc6-47b4-9a61-b5063414683d'),columns:('0b5a3122-8fc6-47b4-9a61-b5063414683d':(dataType:number,isBucketed:!f,label:'Median%20of%20comment_length',operationType:median,scale:ratio,sourceField:comment_length)),incompleteColumns:())))),filters:!(),query:(language:kuery,query:''),visualization:(layers:!((accessors:!('0b5a3122-8fc6-47b4-9a61-b5063414683d'),layerId:'57bae6dc-841f-49e9-85a4-c44b568d8400',layerType:data,position:top,seriesType:bar_stacked,showGridlines:!f)),legend:(isVisible:!t,position:right),preferredSeriesType:bar_stacked,title:'Empty%20XY%20chart',valueLabels:hide,yLeftExtent:(mode:full),yRightExtent:(mode:full))),title:'',type:lens,visualizationType:lnsXY),enhancements:()),gridData:(h:15,i:'6fd55481-beed-40ff-8c3a-b79d4954c081',w:24,x:0,y:0),panelIndex:'6fd55481-beed-40ff-8c3a-b79d4954c081',type:lens,version:'7.17.6')),query:(language:kuery,query:''),tags:!(),timeRestore:!f,title:'YT%20Spam%20Comments',viewMode:edit)&show-query-input=true&show-time-filter=true";
  //document.getElementById("dashboard_frame").setAttribute("src", dashboard_src)

  function handleClick() {
		alert('clicked')
  }

  function youtube_parser() {
    var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
    var match = url_str.match(regExp);
    
    if (match&&match[7].length==11) {
      video_id_str = match[7];
      text_output = "Comment section of YouTube video with ID " + video_id_str + " is being scanned for spam..."
    }
    else {
      video_id_str = ""
      text_output = ""
      url_str = ""
      active = false
      //text_output = "Video ID could not be extracted";
      alert('Video ID could not be extracted! Please enter a valid URL!')
    }
    postVideoId()
    //obtain_spam_comments()
  }

  async function postVideoId() {
    var message;
    const response = await fetch("http://localhost:8000/retrieve_comments/" + video_id_str,
                                {
                                    method: 'POST',
                                    body: JSON.stringify(video_id_str)
                                })
    message = await response.json();
    text_output = message
  }

  // TODO finish and test
  /*
  function obtain_spam_comments() {
    const response = await fetch("http://localhost:8000/spam/" + video_id_str,
                                {
                                    method: 'POST',
                                    body: JSON.stringify(video_id_str)
                                })
    spam_comments = await response;
  }
  */

  // TODO delete?
  /*
  window.setInterval("reloadIFrame();", 30000);
  function reloadIFrame() {
    var frameHolder=document.getElementById('k_dashboard');
    //frameHolder.src=dashboard_src
  }*/

</script>

<svelte:head>
	<link rel="stylesheet" href="https://unpkg.com/mono-icons@1.0.5/iconfont/icons.css" > //for the help icon
</svelte:head>

<main>
<Layout header hideHeader headerHeight={56} let:scroller>
  <div slot="header">
    <div class="header" class:shadow={!!scroller.scroll}>YouTube Spam Scanner</div>
  </div>
  <p class="p">Dear user, welcome to the YouTube Spam Scanner! <span class="wave">👋</span></p>

  <div class="help">
    <div class="question"><i class="mi mi-circle-help"><span class="u-sr-only"></span></i></div>
    <div class="popup">
      <h3>Usage</h3>
      <p>Enter the URL of a YouTube video whose comments you want to check for spam. Click the "Scan" button. Then navigate to the spam comments or dashboards and statistics using the tabs below.</p>
    </div>
  </div>
  
  <div class="internal_div">
    <div class="text_field">
      <input bind:value={url_str} placeholder="Enter the URL of a YouTube video">
    </div>
    <div class="button">
      <button disabled={!url_str} class:active on:click={() => {active=!active}}
        on:click={setTimeout(() => {active = false}, 2000)}
        on:click={youtube_parser}>Scan</button>
    </div>
    <div class="output"><p>{text_output}</p></div>
  </div>

  <div class="container">
    <iframe
    title="dashboard"
    class = "responsive-iframe" src={dashboard_src} frameBorder="0" alt="Kibana is not accessible!!!"></iframe>
  </div>

  <!--
    <h1>The following comments were classified as spam:</h1>
    <ul>
      {#each spam_comments as comment}
        <li>{comment}</li>
      {/each}
    </ul>
  -->

  <!-- <Tabs>
    <TabItem title="Show spam comments">
      <p class="text-sm text-gray-500 dark:text-gray-400"><b>The following comments were classified as spam:</b></p>
      <ul>
        {#each spam_comments as comment}
          <li>{comment}</li>
        {/each}
      </ul>
    </TabItem>
    <TabItem title="Show dashboards">
      <p class="text-sm text-gray-500 dark:text-gray-400"><b>The following dashboards were created:</b> </p> ...
    </TabItem>
  </Tabs> -->
  

</Layout>
</main>


<style>
	main {
    text-align: center;
    /*width: 100%;*/
    /*padding: 25px;*/
    /*max-width: 100%;*/
    /*min-width: 1400px;*/
    /*margin: 0 auto;*/
    background-color: white;
  }
  input {
    width: 500px;
    min-width: 500px;
    height: 30px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
		margin-top: 70px;
		margin-bottom: 50px;
  }
  .internal_div { width: 100%; height: 400px }
  .header {
    background-color: #5ac8fa;
    height: 65px;
    line-height: 65px;
    color: white;
    font-size: 2.5em;
  }
  .responsive-iframe {
    position: relative;
    width: 1500px;
    height: 1800px;
    /*height: 100%;*/
  }
  .container {
    position: relative;
    /*overflow: hidden;*/
    /*padding-top: 2em;*/
    width: auto;
    height: auto;
  }
  .shadow { box-shadow: 0px 2px 8px #00000088; }
	.active {
    background-color: #009688;
    color: white;
  }
  p {
    color: #5ac8fa;
    font-family: 'Comic Sans MS', cursive;
    font-size: 1.5em;
  }
  button {
    height: 4rem;
    width: 10rem;
    background-color: white;
    border-color: #009688;
    color: #009688;
    font-size: 1.25rem;
    background-image: linear-gradient(45deg, #009688 50%, transparent 50%);
    background-position: 100%;
    background-size: 400%;
    transition: background 500ms ease-in-out;
    cursor: pointer;
		margin-bottom: 50px;
  }
  button:hover {
    background-position: 0;
    color: white;
  }
	button:disabled {
		background-image: none;
		border: 1px solid #999999;
		background-color: #cccccc;
		color: #666666;
		cursor: not-allowed;
	}
	.help {
		width: 40px;
		margin: 0 auto;
	}
	.help .question {
		font-size: 25px;
		cursor: pointer;
	}
  .help .popup {
    width: 400px;
    height: 0px;
    text-align: left;
    overflow: hidden;
    position: relative;
    background: #eee;
    opacity: 0;
    transition: 1s;
  }
  .help .popup {
    left: -175px;
    top: 10px;
  }
  .help:hover .popup {
    opacity: 1;
    height: 110px;
  }
  .help .popup h3 {
    margin: 0;
    padding: 10px 0 0 10px;
    height: 30px;
    background: #555;
    color: #fff;
    font-weight: 400;
    font-size: 18px;
  }
  .help .popup p {
    font-size: 14px;
    padding: 10px;
    margin: 0;
    color: #555;
  }

</style>