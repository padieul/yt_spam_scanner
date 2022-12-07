<script>
  import Layout from "./lib/Layout.svelte";
  var url_str = "";
  var text_output = "";

  function handleClick() {
		alert('clicked')
  }

  function youtube_parser(){
    var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*/;
    var match = url_str.match(regExp);

    if (match&&match[7].length==11)
    {
      text_output = match[7];
    }
    else
    {
      text_output = "ID could not be extracted";
    }
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
      <button on:click={youtube_parser}>Get ID</button>
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