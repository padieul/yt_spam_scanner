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
      text_output = "Comment section of Youtube video with ID: " + video_id_str + "is being scanned for spam..."
    }
    else {
      video_id_str = ""
      text_output = "Video ID could not be extracted";
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


<Layout header hideHeader headerHeight={56} let:scroller>
  <div slot="header">
    <div class="header" class:shadow={!!scroller.scroll}>Youtube Spam Scanner</div>
  </div>
  <p>Dear user, welcome to the YouTube Spam Scanner!</p>
  <div class="internal_div">
    <div class="text_field">
      <input bind:value={url_str} placeholder="Enter a URL to a YouTube video">
    </div>
    <div class="button">
      <button class:active on:click={() => {active=!active}}
        on:click={setTimeout(() => {active = false}, 3000)}
        on:click={youtube_parser}>Scan for spam</button>
    </div>
    <div class="output"><p>{text_output}</p></div>
  </div>
</Layout>


<style>
  input {
    width: 500px;
    height: 30px;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    cursor: pointer;
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
    transition: background 300ms ease-in-out;
    cursor: pointer;
  }
  button:hover {
    background-position: 0;
    color: white;
  }
</style>