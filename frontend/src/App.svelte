<script>
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


<main>
  <div>
    <textarea bind:value={url_str}></textarea>
    <button on:click={youtube_parser}>Get ID</button>
    <p>{text_output}</p>
    
  </div>
</main>


<style>
	textarea { width: 100%; height: 200px; }
</style>