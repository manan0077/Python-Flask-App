window.addEventListener('load', function() {
  var form = document.querySelector('form');
  var loading = document.getElementById('loading');

  form.addEventListener('submit', function(event) {
      event.preventDefault();
      var topic = document.getElementById('topic').value;

      // Show loading message
      loading.style.display = 'block';
      
      var xhr = new XMLHttpRequest();
      xhr.open('POST', '/generate', true);
      xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
      xhr.onreadystatechange = function() {
          if (xhr.readyState === 4) {
              // Hide loading message
              loading.style.display = 'none';
              
              if (xhr.status === 200) {
                  var response = xhr.responseText;
                  console.log(response);
                  // Handle the response from the server
                  // Update the page with the generated output
                  document.body.innerHTML = response;
              } else {
                  console.error('Error:', xhr.status);
              }
          }
      };
      xhr.send('topic=' + encodeURIComponent(topic));
  });
});
