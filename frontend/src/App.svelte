<script>
  import Layout from "./lib/Layout.svelte";
  import { Tabs, TabList, TabPanel, Tab } from './lib/tabs.js'; //TODO gehoert das in lib oder in frontend oder in src?

  var url_str = "";
  var text_output = "";
  var test_finish = ""
  var video_id_str = "";
  var active = false;
  var disabled = false;
  var spam_comments = ["Nice song!", "Love it", "Come on.. visit my page!"];

  var dashboard_src = "http://localhost:5601/app/dashboards#/view/3482a810-98f9-11ed-8c04-a96741ae86bb?embed=true&_g=(filters%3A!()%2CrefreshInterval%3A(pause%3A!t%2Cvalue%3A0)%2Ctime%3A(from%3Anow-1y%2Fd%2Cto%3Anow))&show-query-input=true&show-time-filter=true"
  

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
      alert('Video ID could not be extracted! Please enter a valid URL!')
    }
    postVideoId()
    post_obtain_spam_comments()
  }

  async function postVideoId() {
    var message;
    const response = await fetch("http://localhost:8000/retrieve_comments/" + video_id_str,
                                {
                                    method: 'POST',
                                    body: JSON.stringify(video_id_str)
                                })
    message = await response.json();
    console.log(message)
    text_output = message
    test_finish = "YES, postVideoID() finished"
  }

  // TODO finish and test
  async function post_obtain_spam_comments() {
    const response = await fetch("http://localhost:8000/spam/" + video_id_str,
                                {
                                    method: 'POST',
                                    body: JSON.stringify(video_id_str),
                                    headers: {'Content-Type': 'content/type'}
                                })
    spam_comments = await response.json();
    console.log(spam_comments)
    disabled = true;
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
  <p class="p">Dear user, welcome to the YouTube Spam Scanner! <span class="wave">đź‘‹</span></p>

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
    <div class="output"><p>{test_finish}</p></div>
  </div>

  {#if disabled}
  <Tabs>
    <TabList>
      <Tab>Show spam comments</Tab>
      <Tab>Show dashboards</Tab>
    </TabList>
  
    <TabPanel>
      <p class="p">The following comments were classified as spam:</p>
      <ul>
        {#each spam_comments as comment}
          <li>{comment}</li>
        {/each}
      </ul>
    </TabPanel>
  
    <TabPanel>
      <p class="p">The following dashboards were created:</p>
      <div class="container">
        <iframe
        title="dashboard"
        class = "responsive-iframe" src={dashboard_src} frameBorder="0" loading="lazy" allowfullscreen></iframe> <!--alt="Kibana is not accessible!""-->
      </div>
    </TabPanel>
  </Tabs>
  
  {:else}
  <Tabs>
    <TabList>
      <Tab>Show spam comments</Tab>
      <Tab>Show dashboards</Tab>
    </TabList>
  
    <TabPanel>
      <p class="p">The following comments were classified as spam:</p>
    </TabPanel>
  
    <TabPanel>
      <p class="p">The following dashboards were created:</p>
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
  }
  .container {
    position: relative;
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
