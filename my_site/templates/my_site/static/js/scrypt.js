document.querySelectorAll('.social-link').forEach(link => {
  link.addEventListener('click', (event) => {
    alert('Social link clicked!');
  });
});

const carousel = document.querySelector('.carousel');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');

let index = 0;

// Копирование первого и последнего изображения для зацикливания
const images = document.querySelectorAll('.carousel img');
const firstClone = images[0].cloneNode(true);
const lastClone = images[images.length - 1].cloneNode(true);

carousel.appendChild(firstClone);
carousel.insertBefore(lastClone, images[0]);

// Обновляем позиции
const updatePosition = () => {
  const size = images[0].clientWidth;
  carousel.style.transform = `translateX(${-size * (index + 1)}px)`;
};

// Переход к следующему изображению
const nextSlide = () => {
  if (index >= images.length - 1) return;
  index++;
  carousel.style.transition = 'transform 0.5s ease-in-out';
  updatePosition();
};

// Переход к предыдущему изображению
const prevSlide = () => {
  if (index <= 0) return;
  index--;
  carousel.style.transition = 'transform 0.5s ease-in-out';
  updatePosition();
};

// Зацикливание
carousel.addEventListener('transitionend', () => {
  if (images[index].alt === 'Photo 1') {
    index = 0;
    carousel.style.transition = 'none';
    updatePosition();
  }
  // if (images[index].alt === 'Photo 3') {
  //   index = images.length - 2;
  //   carousel.style.transition = 'none';
  //   updatePosition();
  // }
});

// Обработчики событий
nextBtn.addEventListener('click', nextSlide);
prevBtn.addEventListener('click', prevSlide);

// Установка начальной позиции
window.addEventListener('load', updatePosition);

const reviewsCarousel = document.querySelector('.reviews-carousel');
const reviewCards = document.querySelectorAll('.review-card');
const prevReviewBtn = document.querySelector('.review-prev');
const nextReviewBtn = document.querySelector('.review-next');

let reviewIndex = 0;

function updateReviewsPosition() {
  reviewsCarousel.style.transform = `translateX(-${reviewIndex * 320}px)`;
}

nextReviewBtn.addEventListener('click', () => {
  reviewIndex = (reviewIndex + 1) % reviewCards.length;
  updateReviewsPosition();
});

prevReviewBtn.addEventListener('click', () => {
  reviewIndex = (reviewIndex - 1 + reviewCards.length) % reviewCards.length;
  updateReviewsPosition();
});


