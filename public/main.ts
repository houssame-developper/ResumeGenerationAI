if(window.sessionStorage.getItem('token')){
   setTimeout(()=>{
    window.location.href ='downloadPage.html';
   },500)       
}
const form  = document.getElementById("form") as HTMLFormElement;
const  div = document.createElement('div');
div.className = "text-white bg-red-500 p-4 rounded mb-4 fixed w-200 top-10 left-1/2  -translate-x-1/2 z-50"; 
div.textContent = 'Please try again later.';
form.addEventListener('submit',async (event: Event) => {
event.preventDefault();
const  formData:FormData =  new FormData(form)
try{
const response = await fetch('https://philosophical-mae-agentaisoluation-caa8ed9f.koyeb.app/resume/create',{
    method:"POST",
    body:formData
})
if (response.status == 200){
   const reuslt= await response.json();
   window.sessionStorage.setItem("token",reuslt.token);
   setTimeout(()=>{
    window.location.href ='downloadPage.html';
   },500)   
}else{
    setTimeout(() => {
        document.body.appendChild(div);
        setTimeout(() => {
            if (document.body.contains(div)) {
                document.body.removeChild(div);
            }
        }, 2000); 
    }, 1000);
}
}
catch (err) {
document.body.appendChild(div);
}
}
);
