const bodyType = document.getElementById('bodyType');
const bodySuggestion = document.getElementById('bodySuggestion');
const planType = document.getElementById('planType');
const planSuggestion = document.getElementById('planSuggestion');
const caloriesGoal = document.getElementById('caloriesGoal');
const macroGoal = document.getElementById('macroGoal');
const foodGrid = document.getElementById('foodGrid');
const selectedFoods = document.getElementById('selectedFoods');
const menuTotal = document.getElementById('menuTotal');

const bodyProfiles = {
  mesomorfo: {
    text: 'Recomendación: priorizar proteína magra y carbohidrato complejo para potenciar masa muscular.',
    calories: 2400,
    macros: '35/40/25'
  },
  endomorfo: {
    text: 'Recomendación: controlar carga glucémica, aumentar fibra y mantener déficit calórico progresivo.',
    calories: 2000,
    macros: '40/30/30'
  },
  ectomorfo: {
    text: 'Recomendación: superávit calórico con grasas saludables y proteína distribuida en 5 comidas.',
    calories: 2700,
    macros: '30/45/25'
  }
};

const plans = {
  keto: {
    text: 'Menú keto: huevos + aguacate, salmón con ensalada verde, yogurt griego con nueces.',
    foods: [
      { name: 'Huevos + Aguacate', kcal: 420 },
      { name: 'Salmón con espinacas', kcal: 510 },
      { name: 'Yogurt griego + nueces', kcal: 280 }
    ]
  },
  vegano: {
    text: 'Menú vegano: tofu salteado, bowl de quinoa con garbanzos, smoothie de proteína vegetal.',
    foods: [
      { name: 'Tofu salteado', kcal: 350 },
      { name: 'Quinoa + garbanzos', kcal: 480 },
      { name: 'Smoothie vegetal', kcal: 260 }
    ]
  },
  proteico: {
    text: 'Menú proteico: pechuga de pollo, atún con legumbres, omelette con claras.',
    foods: [
      { name: 'Pechuga de pollo', kcal: 390 },
      { name: 'Atún + legumbres', kcal: 440 },
      { name: 'Omelette de claras', kcal: 300 }
    ]
  }
};

const pickedFoods = [];

function renderFoods() {
  const currentPlan = plans[planType.value];
  foodGrid.innerHTML = '';
  currentPlan.foods.forEach((food) => {
    const item = document.createElement('div');
    item.className = 'food-item';
    item.innerHTML = `
      <h4>${food.name}</h4>
      <p>${food.kcal} kcal aprox.</p>
      <button type="button">Agregar</button>
    `;
    item.querySelector('button').addEventListener('click', () => addFood(food));
    foodGrid.appendChild(item);
  });
}

function addFood(food) {
  pickedFoods.push(food);
  const li = document.createElement('li');
  li.textContent = `${food.name} - ${food.kcal} kcal`;
  selectedFoods.appendChild(li);
  const total = pickedFoods.reduce((sum, item) => sum + item.kcal, 0);
  menuTotal.textContent = `${total} kcal`;
}

function updateBodyType() {
  const profile = bodyProfiles[bodyType.value];
  bodySuggestion.textContent = profile.text;
  caloriesGoal.textContent = profile.calories;
  macroGoal.textContent = profile.macros;
}

function updatePlanType() {
  const plan = plans[planType.value];
  planSuggestion.textContent = plan.text;
  renderFoods();
  selectedFoods.innerHTML = '';
  pickedFoods.length = 0;
  menuTotal.textContent = '0 kcal';
}

bodyType.addEventListener('change', updateBodyType);
planType.addEventListener('change', updatePlanType);

updateBodyType();
updatePlanType();
