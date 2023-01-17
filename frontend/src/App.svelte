<script>
  import Layout from "./lib/Layout.svelte";
	import { Tabs, TabItem } from 'flowbite-svelte'; // TODO test if working 

  var url_str = "";
  var text_output = "";
  var video_id_str = "";
  var active = false;
  var spam_comments = ["Nice song!", "Love it", "Come on.. visit my page!"];

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
  <p>Dear user, welcome to the YouTube Spam Scanner! <span class="wave">👋</span></p>

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

  <!--
    <h1>The following comments were classified as spam:</h1>
    <ul>
      {#each spam_comments as comment}
        <li>{comment}</li>
      {/each}
    </ul>
  -->

  <Tabs>
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
  </Tabs>

  <!-- <div class="dashboard_div"> -->
    <iframe title="k_dashoard_title" id="k_dashboard" src="http://kibana:5601/app/dashboards#/view/26cc9470-798b-11ed-a1b0-d777e177c215?embed=true&_g=(filters:!(),refreshInterval:(pause:!t,value:0),time:(from:now-1y%2Fd,to:now))&_a=(description:'Coolest%20dashboard%20ever',filters:!(('$state':(store:appState),meta:(alias:!n,controlledBy:'1670786923045',disabled:!f,index:'55f6f560-7986-11ed-a1b0-d777e177c215',key:_index,negate:!f,params:(query:yt_video_con9k-j4q0u),type:phrase),query:(match_phrase:(_index:yt_video_con9k-j4q0u)))),fullScreenMode:!f,options:(hidePanelTitles:!f,syncColors:!f,useMargins:!t),panels:!((embeddableConfig:(attributes:(description:'',references:!((id:'55f6f560-7986-11ed-a1b0-d777e177c215',name:indexpattern-datasource-current-indexpattern,type:index-pattern),(id:'55f6f560-7986-11ed-a1b0-d777e177c215',name:indexpattern-datasource-layer-853e8e58-ae31-42c1-908f-e4456e8b3d92,type:index-pattern)),state:(datasourceStates:(indexpattern:(layers:('853e8e58-ae31-42c1-908f-e4456e8b3d92':(columnOrder:!(f49f2bf4-06f9-4b74-808f-fbd7c08cb4fc,f2e5f3c8-14c4-4896-a0e8-68e0d0fad094,b255b7d4-13d5-4b93-9fd6-1c9d1ae5d11b),columns:(b255b7d4-13d5-4b93-9fd6-1c9d1ae5d11b:(dataType:number,isBucketed:!f,label:'Count%20of%20records',operationType:count,scale:ratio,sourceField:Records),f2e5f3c8-14c4-4896-a0e8-68e0d0fad094:(dataType:date,isBucketed:!t,label:publish_date,operationType:date_histogram,params:(interval:auto),scale:interval,sourceField:publish_date),f49f2bf4-06f9-4b74-808f-fbd7c08cb4fc:(dataType:boolean,isBucketed:!t,label:'Top%20values%20of%20is_reply',operationType:terms,params:(missingBucket:!f,orderBy:(columnId:b255b7d4-13d5-4b93-9fd6-1c9d1ae5d11b,type:column),orderDirection:desc,otherBucket:!t,size:10),scale:ordinal,sourceField:is_reply)),incompleteColumns:())))),filters:!(),query:(language:kuery,query:''),visualization:(axisTitlesVisibilitySettings:(x:!t,yLeft:!t,yRight:!t),fittingFunction:None,gridlinesVisibilitySettings:(x:!t,yLeft:!t,yRight:!t),labelsOrientation:(x:0,yLeft:0,yRight:0),layers:!((accessors:!(b255b7d4-13d5-4b93-9fd6-1c9d1ae5d11b),layerId:'853e8e58-ae31-42c1-908f-e4456e8b3d92',layerType:data,seriesType:bar_stacked,splitAccessor:f49f2bf4-06f9-4b74-808f-fbd7c08cb4fc,xAccessor:f2e5f3c8-14c4-4896-a0e8-68e0d0fad094)),legend:(isVisible:!t,position:right,shouldTruncate:!t),preferredSeriesType:bar_stacked,tickLabelsVisibilitySettings:(x:!t,yLeft:!t,yRight:!t),valueLabels:hide,yLeftExtent:(mode:full),yRightExtent:(mode:full))),title:'Post%20and%20reply%20over%20time',type:lens,visualizationType:lnsXY),enhancements:()),gridData:(h:11,i:'50a2668d-2d84-4efa-8cbf-7361d15da3e8',w:27,x:0,y:0),panelIndex:'50a2668d-2d84-4efa-8cbf-7361d15da3e8',type:lens,version:'7.17.6'),(embeddableConfig:(enhancements:(),hidePanelTitles:!f,savedVis:(data:(aggs:!(),searchSource:(filter:!(('$state':(store:appState),meta:(alias:!n,controlledBy:'1670786923045',disabled:!f,index:'55f6f560-7986-11ed-a1b0-d777e177c215',key:_index,negate:!f,params:!(yt_video_con9k-j4q0u,yt_video_ruboymzlzkw,yt_video_m5kdztikljm),type:phrases),query:(bool:(minimum_should_match:1,should:!((match_phrase:(_index:yt_video_con9k-j4q0u)),(match_phrase:(_index:yt_video_ruboymzlzkw)),(match_phrase:(_index:yt_video_m5kdztikljm))))))),query:(language:kuery,query:''))),description:'',id:'',params:(controls:!((fieldName:_index,id:'1670786923045',indexPattern:'55f6f560-7986-11ed-a1b0-d777e177c215',label:'',options:(dynamicOptions:!t,multiselect:!t,order:desc,size:5,type:terms),parent:'',type:list),(fieldName:'',id:'1670786941039',indexPattern:'',label:'',options:(dynamicOptions:!t,multiselect:!t,order:desc,size:5,type:terms),parent:'',type:list)),pinFilters:!f,updateFiltersOnChange:!f,useTimeFilter:!f),title:'',type:input_control_vis,uiState:())),gridData:(h:10,i:'2dd1a0a0-af36-4191-91e0-855a6258b65a',w:21,x:27,y:0),panelIndex:'2dd1a0a0-af36-4191-91e0-855a6258b65a',title:'Select%20Video',type:visualization,version:'7.17.6'),(embeddableConfig:(attributes:(references:!((id:'55f6f560-7986-11ed-a1b0-d777e177c215',name:indexpattern-datasource-current-indexpattern,type:index-pattern),(id:'55f6f560-7986-11ed-a1b0-d777e177c215',name:indexpattern-datasource-layer-d1bb6067-be8d-4a4d-a8b5-ee510c218644,type:index-pattern)),state:(datasourceStates:(indexpattern:(layers:(d1bb6067-be8d-4a4d-a8b5-ee510c218644:(columnOrder:!('35e7bf5c-9e62-4a1a-802a-1664275ab90a','13f26e63-4f94-4016-9785-77758e7fe791',b171663a-bb26-4f29-94a6-383d9dd544be),columns:('13f26e63-4f94-4016-9785-77758e7fe791':(dataType:date,isBucketed:!t,label:publish_date,operationType:date_histogram,params:(interval:auto),scale:interval,sourceField:publish_date),'35e7bf5c-9e62-4a1a-802a-1664275ab90a':(dataType:string,isBucketed:!t,label:'Top%20values%20of%20_index',operationType:terms,params:(missingBucket:!f,orderBy:(columnId:b171663a-bb26-4f29-94a6-383d9dd544be,type:column),orderDirection:desc,otherBucket:!t,size:3),scale:ordinal,sourceField:_index),b171663a-bb26-4f29-94a6-383d9dd544be:(dataType:number,isBucketed:!f,label:'Median%20of%20comment_length',operationType:median,scale:ratio,sourceField:comment_length)),incompleteColumns:())))),filters:!(),query:(language:kuery,query:''),visualization:(gridConfig:(isCellLabelVisible:!f,isXAxisLabelVisible:!t,isYAxisLabelVisible:!t,type:lens_heatmap_grid),layerId:d1bb6067-be8d-4a4d-a8b5-ee510c218644,layerType:data,legend:(isVisible:!t,position:right,type:lens_heatmap_legendConfig),palette:(accessor:b171663a-bb26-4f29-94a6-383d9dd544be,name:custom,params:(colorStops:!((color:%236092c0,stop:0),(color:%23a8bfda,stop:20),(color:%2354B399,stop:40),(color:%23ecb385,stop:60),(color:%23e7664c,stop:80)),name:custom,rangeMax:80,rangeMin:0,steps:5,stops:!((color:%236092c0,stop:20),(color:%23a8bfda,stop:40),(color:%2354B399,stop:60),(color:%23ecb385,stop:80),(color:%23e7664c,stop:100))),type:palette),shape:heatmap,valueAccessor:b171663a-bb26-4f29-94a6-383d9dd544be,xAccessor:'13f26e63-4f94-4016-9785-77758e7fe791',yAccessor:'35e7bf5c-9e62-4a1a-802a-1664275ab90a')),title:'',type:lens,visualizationType:lnsHeatmap),enhancements:(),hidePanelTitles:!f),gridData:(h:14,i:'73e4fc61-dc71-4b71-af45-e0059f64c9ff',w:21,x:27,y:10),panelIndex:'73e4fc61-dc71-4b71-af45-e0059f64c9ff',title:'Median%20length%20of%20comment%20over%20time',type:lens,version:'7.17.6'),(embeddableConfig:(enhancements:()),gridData:(h:13,i:'6287ba48-0171-40a3-a2cf-ab4ad38c3a6b',w:27,x:0,y:11),id:e0d8a140-7988-11ed-a1b0-d777e177c215,panelIndex:'6287ba48-0171-40a3-a2cf-ab4ad38c3a6b',type:lens,version:'7.17.6'),(embeddableConfig:(attributes:(references:!((id:'55f6f560-7986-11ed-a1b0-d777e177c215',name:indexpattern-datasource-current-indexpattern,type:index-pattern),(id:'55f6f560-7986-11ed-a1b0-d777e177c215',name:indexpattern-datasource-layer-ce32193a-63c0-4532-8f97-f65ecfb044d6,type:index-pattern)),state:(datasourceStates:(indexpattern:(layers:(ce32193a-63c0-4532-8f97-f65ecfb044d6:(columnOrder:!(d5c1afc0-2331-4b6b-8b0a-ac9b145464d0,'829e9df8-277a-4a56-ab1f-74cb10ed3628'),columns:('829e9df8-277a-4a56-ab1f-74cb10ed3628':(dataType:number,isBucketed:!f,label:'Count%20of%20records',operationType:count,scale:ratio,sourceField:Records),d5c1afc0-2331-4b6b-8b0a-ac9b145464d0:(dataType:string,isBucketed:!t,label:'Top%20values%20of%20author_name.keyword',operationType:terms,params:(missingBucket:!f,orderBy:(columnId:'829e9df8-277a-4a56-ab1f-74cb10ed3628',type:column),orderDirection:desc,otherBucket:!f,size:50),scale:ordinal,sourceField:author_name.keyword)),incompleteColumns:())))),filters:!(),query:(language:kuery,query:''),visualization:(layers:!((categoryDisplay:default,groups:!(d5c1afc0-2331-4b6b-8b0a-ac9b145464d0),layerId:ce32193a-63c0-4532-8f97-f65ecfb044d6,layerType:data,legendDisplay:default,legendMaxLines:2,metric:'829e9df8-277a-4a56-ab1f-74cb10ed3628',nestedLegend:!f,numberDisplay:percent)),shape:pie)),title:'',type:lens,visualizationType:lnsPie),enhancements:(),hidePanelTitles:!f),gridData:(h:19,i:f43d595e-77a9-4ebd-a592-87c2fa9ac1ee,w:23,x:0,y:24),panelIndex:f43d595e-77a9-4ebd-a592-87c2fa9ac1ee,title:'Most%20active%20channels%20by%20name',type:lens,version:'7.17.6'),(embeddableConfig:(attributes:(references:!((id:'55f6f560-7986-11ed-a1b0-d777e177c215',name:indexpattern-datasource-current-indexpattern,type:index-pattern),(id:'55f6f560-7986-11ed-a1b0-d777e177c215',name:indexpattern-datasource-layer-c4818321-3d6b-4632-aa2c-c556b1a6bc3b,type:index-pattern)),state:(datasourceStates:(indexpattern:(layers:(c4818321-3d6b-4632-aa2c-c556b1a6bc3b:(columnOrder:!('417912ff-cf51-4361-9612-0ca2bb827d19','103a5762-45e9-4b98-94f0-ac2c5e8a6ae5',c3b878d7-afaa-42aa-96d0-4459ab90bdba,c823764c-347f-460b-b92f-b805060bb378,'67a22a61-1fb0-4ba4-b92d-76cdb31b0dd6'),columns:('103a5762-45e9-4b98-94f0-ac2c5e8a6ae5':(dataType:string,isBucketed:!t,label:'Top%20values%20of%20content.keyword',operationType:terms,params:(missingBucket:!f,orderBy:(columnId:c3b878d7-afaa-42aa-96d0-4459ab90bdba,type:column),orderDirection:desc,otherBucket:!t,size:3),scale:ordinal,sourceField:content.keyword),'417912ff-cf51-4361-9612-0ca2bb827d19':(dataType:string,isBucketed:!t,label:'Top%20values%20of%20author_name.keyword',operationType:terms,params:(missingBucket:!f,orderBy:(columnId:c3b878d7-afaa-42aa-96d0-4459ab90bdba,type:column),orderDirection:desc,otherBucket:!t,size:5),scale:ordinal,sourceField:author_name.keyword),'67a22a61-1fb0-4ba4-b92d-76cdb31b0dd6':(dataType:number,isBucketed:!f,label:'Median%20of%20like_count',operationType:median,scale:ratio,sourceField:like_count),c3b878d7-afaa-42aa-96d0-4459ab90bdba:(dataType:number,isBucketed:!f,label:'Count%20of%20records',operationType:count,scale:ratio,sourceField:Records),c823764c-347f-460b-b92f-b805060bb378:(dataType:number,isBucketed:!f,label:'Median%20of%20comment_length',operationType:median,scale:ratio,sourceField:comment_length)),incompleteColumns:())))),filters:!(),query:(language:kuery,query:''),visualization:(columns:!((columnId:'417912ff-cf51-4361-9612-0ca2bb827d19',isTransposed:!f),(columnId:'103a5762-45e9-4b98-94f0-ac2c5e8a6ae5',isTransposed:!f),(columnId:c3b878d7-afaa-42aa-96d0-4459ab90bdba,isTransposed:!f),(columnId:c823764c-347f-460b-b92f-b805060bb378,isTransposed:!f),(columnId:'67a22a61-1fb0-4ba4-b92d-76cdb31b0dd6',isTransposed:!f)),layerId:c4818321-3d6b-4632-aa2c-c556b1a6bc3b,layerType:data)),title:'',type:lens,visualizationType:lnsDatatable),enhancements:()),gridData:(h:19,i:'9c413e78-031b-420b-8e80-9f3be1835e78',w:25,x:23,y:24),panelIndex:'9c413e78-031b-420b-8e80-9f3be1835e78',type:lens,version:'7.17.6')),query:(language:kuery,query:''),tags:!(),timeRestore:!f,title:'Youtube%20Spam%20Comments',viewMode:view)&show-top-menu=true&show-query-input=true&show-time-filter=true"  height="1000" width="1000" ></iframe>
  

</Layout>
</main>


<style>
	main {
    text-align: center;
    padding: 4em;
    max-width: 1000px;
    margin: 0 auto;
  }
  input {
    width: 500px;
    height: 30px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
		margin-top: 70px;
		margin-bottom: 50px;
  }
  .internal_div {width: 100%; height: 400px}
  /* .dashboard_div {width: 100%; height: 100%} */
  .header {
    background-color: #5ac8fa;
    height: 65px;
    line-height: 65px;
    color: white;
    padding-left: 16px;
    font-size: 2.5em;
  }
  .shadow { box-shadow: 0px 2px 8px #00000088;}
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