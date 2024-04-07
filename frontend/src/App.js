import logo from './logo.svg';
import './App.css';
import React, { useState } from 'react';

const apiUrl = `${process.env.REACT_APP_API_BASE_URL}/analyze`;
alert(apiUrl)

function FileUpload() {
  const [file, setFile] = useState(null);

  const handleFileChange = event => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!file) {
      alert('Please select a file first!');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(apiUrl, {
          method: 'POST',
          body: formData,
      });

      // Check the response type
      const contentDisposition = response.headers.get('Content-Disposition');
      //const filename = getFilenameFromContentDisposition(contentDisposition);
      if (contentDisposition) {
          // Handle file download
          const filename = contentDisposition.split('filename=')[1].split(';')[0].replace(/"/g, '');
          const blob = await response.blob();
          const downloadUrl = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = downloadUrl;
          a.download = filename; // you can get the filename from Content-Disposition header
          document.body.appendChild(a);
          a.click();
          a.remove();
      } else {
          // Handle JSON response
          const data = await response.json();
          console.log(data);
          alert('Received JSON response');
      }
    } catch (error) {
        console.error('Error:', error);
        alert('Error uploading file');
    }
  };

  
  return (
    
    <form onSubmit={handleSubmit}>
      <img src={logo} className="App-logo" alt="logo" />
      <label>
        Upload file:
        <input type="file" onChange={handleFileChange} />
      </label>
      <button type="submit">Upload</button>
    </form>
  );
}

export default FileUpload;

