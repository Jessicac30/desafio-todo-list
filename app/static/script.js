let tasks = [];
let categories = [];
let selectedCategory = null;

const saveLocal = () => {
  localStorage.setItem("tasks", JSON.stringify(tasks));
};

const getLocal = () => {
  const tasksLocal = JSON.parse(localStorage.getItem("tasks"));
  if (tasksLocal) {
    tasks = tasksLocal;
  }
};

const toggleScreen = () => {
  screenWrapper.classList.toggle("show-category");
};

const updateTotals = () => {
  const categoryTasks = tasks.filter(
    (task) => task.category_id === selectedCategory?.id
  );

  numTasks.innerHTML = `${categoryTasks.length || 0} Tarefas`;
  totalTasks.innerHTML = tasks.length;
};

const redirectToLogin = () => {
  window.location.href = '/';
};


const checkAuthentication = (response) => {
  if (response.status === 401) {
    localStorage.removeItem('access_token');
    redirectToLogin();
    throw new Error('Token inválido ou expirado');
  }
  return response;
};


const loadCategories = () => {
  fetch('/api/categories', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }
  })
  .then(checkAuthentication)
  .then(response => response.json())
  .then(data => {
    categories = data;
    loadTasks();
    populateCategorySelect();
  })
  .catch(error => console.error('Error loading categories:', error));
};

const loadTasks = () => {
  fetch('/api/tasks', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }
  })
  .then(checkAuthentication)
  .then(response => response.json())
  .then(tasksData => {
    tasks = tasksData;
    renderCategories();
    totalTasks.innerHTML = tasks.length;
  })
  .catch(error => console.error('Error loading tasks:', error));
};

const populateCategorySelect = () => {
  categorySelect.innerHTML = '';
  categories.forEach((category) => {
    const option = document.createElement("option");
    option.value = category.id;
    option.textContent = category.title;
    categorySelect.appendChild(option);
  });
};

const renderCategories = () => {
  categoriesContainer.innerHTML = '';
  categories.forEach((category) => {
    const categoryTaskCount = tasks.filter(task => task.category_id === category.id).length;

    const div = document.createElement("div");
    div.classList.add("category");

    div.addEventListener("click", () => {
      selectedCategory = category;
      fetchCategoryTasks(category);
    });

    div.innerHTML = `
      <div class="left">
        <img src="../static/images/${category.img}" alt="${category.title}" />
        <div class="content">
          <h1>${category.title}</h1>
          <p>${categoryTaskCount || 0} Tarefas</p>
        </div>
      </div>
      <div class="options">
        <div class="toggle-btn">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 12.75a.75.75 0 110-1.5.75.75 0 010 1.5zM12 18.75a.75.75 0 110-1.5.75.75 0 010 1.5z"/>
          </svg>
        </div>
      </div>
    `;

    categoriesContainer.appendChild(div);
  });
};

const fetchCategoryTasks = (category) => {
  fetch(`/api/categories/${category.id}/tasks`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }
  })
  .then(checkAuthentication)
  .then(response => response.json())
  .then(tasksData => {
    tasks = tasksData;
    categoryTitle.innerHTML = category.title;
    categoryImg.src = `../static/images/${category.img}`;
    renderTasks();
    updateTotals();
    toggleScreen();
  })
  .catch(error => console.error('Error fetching tasks:', error));
};

const renderTasks = () => {
  tasksContainer.innerHTML = '';
  const categoryTasks = tasks.filter(
    (task) => task.category_id === selectedCategory.id
  );

  if (categoryTasks.length === 0) {
    tasksContainer.innerHTML = `<p class="no-tasks">Nenhuma tarefa adicionada para esta categoria</p>`;
  } else {
    categoryTasks.forEach((task) => {
      const div = document.createElement("div");
      div.classList.add("task-wrapper");
      const label = document.createElement("label");
      label.classList.add("task");
      label.setAttribute("for", task.id);
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.id = task.id;
      checkbox.checked = task.completed;
      checkbox.addEventListener("change", () => {
        updateTaskStatus(task.id, !task.completed);
      });

      div.innerHTML = `
        <div class="delete">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0"/>
          </svg>
        </div>
      `;

      label.innerHTML = `
        <span class="checkmark">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5"/>
          </svg>
        </span>
        <p>${task.title}</p>
      `;
      label.prepend(checkbox);
      div.prepend(label);
      tasksContainer.appendChild(div);

      const deleteBtn = div.querySelector(".delete");
      deleteBtn.addEventListener("click", () => {
        deleteTask(task.id);
      });
    });

    updateTotals();
  }
};

const toggleAddTaskForm = () => {
  addTaskWrapper.classList.toggle("active");
  blackBackdrop.classList.toggle("active");
  addTaskBtn.classList.toggle("active");
};

const addTask = (e) => {
  e.preventDefault();
  const taskTitle = taskInput.value;
  const category = categorySelect.value;

  if (taskTitle === "") {
    alert("Por favor, insira uma tarefa");
  } else {
    const newTask = {
      title: taskTitle,
      category_id: category
    };
    taskInput.value = "";
    createTask(newTask);
  }
};

const createTask = (task) => {
  fetch('/api/tasks', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    },
    body: JSON.stringify(task),
  })
  .then(checkAuthentication)
  .then(response => response.json())
  .then(data => {
    tasks.push(data);
    saveLocal();
    toggleAddTaskForm();
    renderTasks();
    updateTotals();
    populateCategorySelect();
    loadTasks(); 
  })
  .catch(error => console.error('Error:', error));
};

const updateTaskStatus = (taskId, completed) => {
  fetch(`/api/tasks/${taskId}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    },
    body: JSON.stringify({ completed }),
  })
  .then(checkAuthentication)
  .then(response => response.json())
  .then(data => {
    const index = tasks.findIndex(t => t.id === taskId);
    tasks[index].completed = completed;
    saveLocal();
    renderTasks();
    updateTotals();
    loadTasks(); 
  })
  .catch(error => console.error('Error:', error));
};

const deleteTask = (taskId) => {
  fetch(`/api/tasks/${taskId}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${localStorage.getItem('access_token')}`
    }
  })
  .then(() => {
    const index = tasks.findIndex(t => t.id === taskId);
    tasks.splice(index, 1);
    saveLocal();
    renderTasks();
    updateTotals();
    loadTasks(); 
  })
  .catch(error => console.error('Error:', error));
};

const categoriesContainer = document.querySelector(".categories");
const screenWrapper = document.querySelector(".wrapper");
const menuBtn = document.querySelector(".menu-btn");
const backBtn = document.querySelector(".back-btn");
const tasksContainer = document.querySelector(".tasks");
const numTasks = document.getElementById("num-tasks");
const categoryTitle = document.getElementById("category-title");
const categoryImg = document.getElementById("category-img");
const categorySelect = document.getElementById("category-select");
const addTaskWrapper = document.querySelector(".add-task");
const addTaskBtn = document.querySelector(".add-task-btn");
const taskInput = document.getElementById("task-input");
const blackBackdrop = document.querySelector(".black-backdrop");
const addBtn = document.querySelector(".add-btn");
const cancelBtn = document.querySelector(".cancel-btn");
const totalTasks = document.getElementById("total-tasks");

menuBtn.addEventListener("click", toggleScreen);
backBtn.addEventListener("click", toggleScreen);
addTaskBtn.addEventListener("click", toggleAddTaskForm);
blackBackdrop.addEventListener("click", toggleAddTaskForm);
addBtn.addEventListener("click", addTask);
cancelBtn.addEventListener("click", toggleAddTaskForm);


getLocal();
loadCategories();
