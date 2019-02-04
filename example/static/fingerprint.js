function fingerprint(file, callback) {
  var blobSlice = File.prototype.slice || File.prototype.mozSlice || File.prototype.webkitSlice;
  var chunkSize = 1048576;                        // Read in chunks of 2MB
  var chunks = Math.ceil(file.size / chunkSize);  // Total chunks to be sent
  var currentChunk = 0;                           // State of hash
  var spark = new SparkMD5.ArrayBuffer();
  var fileReader = new FileReader();

  fileReader.onload = function (e) {
    spark.append(e.target.result); // Append array buffer
    currentChunk++;

    if (currentChunk < chunks) {
      loadNext();
    } else {
      return callback(spark.end())
    }
  };

  fileReader.onerror = function () {
    console.warn('Error occured');
  };

  function loadNext() {
    var start = currentChunk * chunkSize;
    var end = ((start + chunkSize) >= file.size) ? file.size : start + chunkSize;
    fileReader.readAsArrayBuffer(blobSlice.call(file, start, end));
  }

  loadNext();
};
