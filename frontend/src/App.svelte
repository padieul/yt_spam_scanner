<script>
  import Layout from "./lib/Layout.svelte";
  var url_str = "";
  var text_output = "";
  var video_id_str = "";

  function handleClick() {
		alert('clicked')
  }

  function youtube_parser(){
    var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
    var match = url_str.match(regExp);
    

    if (match&&match[7].length==11)
    {
      video_id_str = match[7];
      text_output = "Comment section of Youtube video with ID: " + video_id_str + "is being scanned for spam..."
    }
    else
    {
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
    <div class="header" class:shadow={!!scroller.scroll}>
			Youtube Spam Scanner
		</div>
  </div>

  <div class="internal_div">
  
    <div class="text_field">
      <input bind:value={url_str}>
    </div>
    <div class="button">
      <button on:click={youtube_parser}>Scan</button>
    </div>
    <div class="output">
      <p>{text_output}</p>
    </div>
    
  </div>

</Layout>



<style>
  input { width: 500px; height: 25px; }

  button {background-color: aqua; }

  .internal_div {width: 100%; height: 300px}

  .header {
		background-color: #FF0000;
		height: 56px;
		line-height: 56px;
		color: #FFFFFF;
		padding-left: 16px;
	}
	
	.shadow {
  	box-shadow: 0px 2px 8px #00000088;
	}
</style>