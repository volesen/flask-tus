function fingerprint(file) {
  var blobSlice = File.prototype.slice || File.prototype.mozSlice || File.prototype.webkitSlice,
  var chunkSize = 1048576, // Read in chunks of 2MB
  var chunks = Math.ceil(file.size / chunkSize), // Total chunks to be sent
  var currentChunk = 0, // State of hash
  var spark = new SparkMD5.ArrayBuffer(),
  var fileReader = new FileReader();

  fileReader.onload = function(e) {
    console.log('read chunk nr', currentChunk + 1, 'of', chunks);
    spark.append(e.target.result); // Append array buffer
    currentChunk++;

    if (currentChunk < chunks) {
      loadNext();
    } else {
      console.info('computed hash', spark.end()); // Compute hash
    }
  };

  fileReader.onerror = function() {
    console.warn('oops, something went wrong.');
  };

  function loadNext() {
    var start = currentChunk * chunkSize,
    var end = ((start + chunkSize) >= file.size) ? file.size : start + chunkSize;

    fileReader.readAsArrayBuffer(blobSlice.call(file, start, end));
  }

  loadNext();
};
