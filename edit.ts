const token = window.sessionStorage.getItem('token');
const elementDiv = document.createElement('div');
elementDiv.className = "text-white bg-red-500 p-4 rounded mb-4 fixed w-200 top-10 left-1/2  -translate-x-1/2 z-50";

if (!token) {
  elementDiv.textContent = "Your token has expired. Please fill the resume form again.";
  document.body.appendChild(elementDiv);
  setTimeout(() => {
    window.location.href = 'main.html';
  }, 1500);
}

let data: { [key: string]: string } = {};
const formEdit = document.getElementById("form") as HTMLFormElement;

document.addEventListener('DOMContentLoaded', async () => {
  try {
    const response = await fetch(`http://127.0.0.1:8000/resume/${token}`, {
      method: "GET",
      headers: { "Content-Type": "application/json" },
    });

    if (response.status === 200) {
      const result = await response.json();
      data = result.response;

      for (const key in data) {
        const input = document.querySelector(`[name="${key}"]`) as HTMLInputElement;
        if (input && input.type !== "file") {
          input.value = data[key];
        }
      }

      const resume_id: number = parseInt(data.id);

      formEdit.addEventListener('submit', async (event: Event) => {
        event.preventDefault();
        const formData: FormData = new FormData(formEdit);
        if (!data.photo) data.photo = "No add photo section";

        try {
          const res = await fetch(`http://127.0.0.1:8000/resume/update/${resume_id}`, {
            method: "PUT",
            body: formData,
          });

          if (res.status === 200) {
            setTimeout(() => {
              window.location.href = 'downloadPage.html';
            }, 500);
          } else {
            elementDiv.textContent = "Please try again later.";
            document.body.appendChild(elementDiv);
            setTimeout(() => {
              document.body.removeChild(elementDiv);
            }, 2000);
          }
        } catch (err) {
          document.body.appendChild(elementDiv);
        }
      });
    } else {
      elementDiv.textContent = "Please try again later.";
      document.body.appendChild(elementDiv);
      setTimeout(() => {
        document.body.removeChild(elementDiv);
      }, 2000);
    }
  } catch (err) {
    elementDiv.textContent = "Server error.";
    document.body.appendChild(elementDiv);
  }
});
