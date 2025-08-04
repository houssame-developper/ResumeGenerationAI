document.addEventListener('DOMContentLoaded', () => {
  const token = window.sessionStorage.getItem('token');
  const fileInstall = document.getElementById('install') as HTMLButtonElement;
  const editButton = document.getElementById('edit') as HTMLButtonElement;

  const div1 = document.createElement('div');
const loadingOverlay = document.getElementById('loading-overlay');

if (!token) {
    div1.textContent = "Your token has expired. Please fill the resume form again.";
    setTimeout(() => {
      document.body.appendChild(div1);
      window.location.href = 'main.html';
      setTimeout(() => {
        if (document.body.contains(div1)) {
          document.body.removeChild(div1);
        }
      }, 2000);
    }, 1000);
    return; // نوقف تنفيذ الباقي
  }

  div1.textContent = "You can't install file. Please try again later.";

  fileInstall.addEventListener('click', async () => {
    try {
      if(loadingOverlay){
         loadingOverlay.classList.remove('hidden');
 
      }
      const response = await fetch(`https://philosophical-mae-agentaisoluation-caa8ed9f.koyeb.app/user/${token}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        }
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = "resume.pdf";
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);
      } else {
        document.body.appendChild(div1);
        setTimeout(() => {
          if (document.body.contains(div1)) {
            document.body.removeChild(div1);
          }
        }, 2000);
      }
    } catch (err) {
      console.error(err);
      document.body.appendChild(div1);
      setTimeout(() => {
        if (document.body.contains(div1)) {
          document.body.removeChild(div1);
        }
      }, 2000);
    }finally {
      if(loadingOverlay){
          loadingOverlay.classList.add('hidden');

      }    }
  });

editButton.addEventListener('click',()=>{
  setTimeout(()=>{
    window.location.href = 'edit.html';
  },500)
})
});

