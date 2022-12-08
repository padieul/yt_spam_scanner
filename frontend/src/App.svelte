<script>
  import Layout from "./lib/Layout.svelte";
  var url_str = "";
  var text_output = "";
  var video_id_str = "";
  var active = false;
  
  function handleClick() {
		alert('clicked')
  }

  function youtube_parser(){
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
  }

  async function postVideoId(){
    var message;
    const response = await fetch("http://localhost:8000/retrieve_comments/" + video_id_str,
                                {
                                    method: 'POST',
                                    body: JSON.stringify(video_id_str)
                                })
    message = await response.json();
    text_output = message
  }

</script>

<main>
<Layout header hideHeader headerHeight={56} let:scroller>
  <div slot="header">
    <div class="header" class:shadow={!!scroller.scroll}>YouTube Spam Scanner</div>
  </div>
  <p>Dear user, welcome to the YouTube Spam Scanner! <span class="wave">👋</span></p>
  <div class="internal_div">
    <div class="text_field">
      <input bind:value={url_str} placeholder="Enter the URL of a YouTube video">
    </div>
    <div class="button">
      <button disabled={!url_str} class:active on:click={() => {active=!active}}
        on:click={setTimeout(() => {active = false}, 2000)}
        on:click={youtube_parser}>Scan</button>
    </div>
		<div class="help">
		<div class="question">?</div>
		<div class="popup">
			<h3>Usage</h3>
			<p>Enter the URL of a YouTube video whose comments you want to check for spam. Then click the button. Optionally, select one or more options for the visualizations and statistics you want to obtain.</p>
		</div>
		</div>
    <div class="output"><p>{text_output}</p></div>
  </div>
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
		height: 35px;
		width: 35px;
		background: #ccc;
		font-size: 25px;
		line-height: 32px;
		text-align: center;
		border-radius: 50%;
		cursor: help;
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
    height: 150px;
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