<script>
  import Layout from "./lib/Layout.svelte";
  import { Tabs, TabList, TabPanel, Tab } from './lib/tabs.js'; //TODO gehoert das in lib oder in frontend oder in src?

  var url_str = "";
  var video_id_str = "";
  var active_scan_button = false;
  var active_dashboard = false;
  var text_scanning_status = "";
  var text_post_request_status = "";
  var text_get_request_status  = "";
  var spam_comments = [];
  var number_spam = 0; // spomments
  var number_comments = 0; // total

  var dashboard_src = "http://localhost:5601/app/dashboards#/view/3482a810-98f9-11ed-8c04-a96741ae86bb?embed=true&_g=(filters%3A!()%2CrefreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3Anow-1y%2Fd%2Cto%3Anow))&show-query-input=true&show-time-filter=true"


  function delay(milliseconds){
    return new Promise(resolve => {
        setTimeout(resolve, milliseconds);
    });
 }


  async function youtube_parser() {
    // hide process steps, spomments and dashboards from previous scan
    text_scanning_status = "";
    text_post_request_status = "";
    text_get_request_status = "";
    active_dashboard = false;
    
    // extract the video id from the given YouTube video URL
    var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
    var match = url_str.match(regExp);
    
    if (match&&match[7].length==11) {
      video_id_str = match[7];
      text_scanning_status = "Please wait: The comment section of the YouTube video with ID " + video_id_str + " is being scanned for spam..."
    }
    else {
      video_id_str = ""
      url_str = ""
      active_scan_button = false
      alert('The video ID could not be extracted! Please enter a valid URL!')
    }
    text_post_request_status = await postVideoId()
    await delay(1500);
    text_get_request_status = await obtain_spam_comments()
  }


  // retrieve comments and store them in ES
  async function postVideoId() {
    var message;
    const response = await fetch("http://localhost:8000/retrieve_comments/" + video_id_str,
                                {
                                  method: 'POST',
                                  mode: 'cors',
                                  body: JSON.stringify(video_id_str)
                                });
    message = await response.json();
    //console.log("COMMENTS RETRIEVED")
    return "(1/2) The comments have been successfully obtained."
  }


  // get the comments labeled as spam
  async function obtain_spam_comments() {
    var message;
    const response = await fetch("http://localhost:8000/spam/" + video_id_str,
                                {
                                  method: 'GET',
                                  mode: 'cors'
                                });
    message = await response.json()
    //console.log("SPAM COMMENTS RETRIEVED")
    spam_comments = message["spam"];
    number_spam = message["spam_count"];
    number_comments = message["total_count"];
    active_dashboard = true;
    return "(2/2) The comments have been successfully classified."
  }  

</script>

<svelte:head>
	<link rel="stylesheet" href="https://unpkg.com/mono-icons@1.0.5/iconfont/icons.css" > <!--for the help icon-->
</svelte:head>

<main>
<Layout header hideHeader headerHeight={56} let:scroller>
  <div slot="header">
    <div class="header" class:shadow={!!scroller.scroll}>YouTube Spam Scanner</div>
  </div>
  <p class="p">Dear user, welcome to the YouTube Spam Scanner!</p>

  <div class="help">
    <div class="question"><i class="mi mi-circle-help"><span class="u-sr-only"></span></i></div>
    <div class="popup">
      <h3>Usage</h3>
      <p>Enter the URL of a YouTube video whose comments you want to check for spam. Click the "Scan" button. Then navigate to the spam comments (spomments) or dashboard and statistics using the tabs below.</p>
    </div>
  </div>
  
  <div class="internal_div">
    <div class="text_field">
      <input bind:value={url_str} placeholder="Enter the URL of your YouTube video">
    </div>
    <div class="button">
      <button disabled={!url_str} class:active_scan_button on:click={() => {active_scan_button=!active_scan_button}}
        on:click={setTimeout(() => {active_scan_button = false}, 2000)}
        on:click={youtube_parser}>Scan</button>
    </div>
    <output>{text_scanning_status}<br>{text_post_request_status}<br>{text_get_request_status}</output>
  </div>

  {#if active_dashboard}
  <Tabs>
    <TabList>
      <Tab>Spomments</Tab>
      <Tab>Dashboard</Tab>
    </TabList>
  
    <TabPanel>
      <p class="p">The following {number_spam} out of {number_comments} comments on your video have been classified as spam:</p>
      <ul>
        {#each spam_comments as comment}
          <li>{comment}</li>
        {/each}
      </ul>
    </TabPanel>
  
    <TabPanel>
      <p class="p">The following dashboards have been created for your video:</p>
      <div class="container">
        <iframe
        title="dashboard"
        class = "responsive_iframe" src={dashboard_src} frameBorder="0" loading="lazy" allowfullscreen></iframe>
      </div>
    </TabPanel>
  </Tabs>
  
  {:else}
  <Tabs>
    <TabList>
      <Tab>Spomments</Tab>
      <Tab>Dashboard</Tab>
    </TabList>
  
    <TabPanel>
      <p class="p">No video URL has been entered yet...</p>
    </TabPanel>
  
    <TabPanel>
      <p class="p">No video URL has been entered yet...</p>
    </TabPanel>
  </Tabs>
  {/if}

</Layout>
</main>


<style>
	main {
    text-align: center;
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
  output {
    color: #5ac8fa;
    font-family: 'Comic Sans MS', cursive;
    font-size: 1.2em;
		line-height: 2.5;
	}
  li {
    text-align: left;
  }
  .internal_div { width: 100%; height: 450px }
  .header {
    background-color: #5ac8fa;
    height: 65px;
    line-height: 65px;
    color: white;
    font-size: 2.5em;
  }
  .responsive_iframe {
    position: relative;
    width: 1500px;
    height: 1800px;
  }
  .container {
    position: relative;
    width: auto;
    height: auto;
  }
  .shadow { box-shadow: 0px 2px 8px #00000088; }
	.active_scan_button {
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
    left: -184px;
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
    text-align: center;
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
