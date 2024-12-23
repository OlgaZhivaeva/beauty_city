let selectedSalonId = null;  // Переменная для хранения id выбранного салона
let selectedServiceId = null;  // Переменная для хранения id выбранной услуги
let selectedMasterId = null;  // Переменная для хранения id выбранного мастера
$(document).ready(function() {
  // Обработчик события клика по кнопкам выбора салона
  $('#salon-panel .accordion__block').click(function () {
    selectedSalonId = $(this).data('id');
    $('#select-service-btn').prop('disabled', false); // Активируем кнопку выбора услуги
  });

  // Обработчик события клика по услугам
  $('.accordion__block_item').click(function () {
    selectedServiceId = $(this).data('id'); // Извлекаем id услуги
    if (!selectedSalonId || !selectedServiceId) return;

    $.ajax({
      url: '/get_masters/', // URL для получения мастеров
      method: 'GET',
      data: {
        salon_id: selectedSalonId,
        service_id: selectedServiceId,
      },
      success: function (response) {
        updateMastersPanel(response.masters);
      },
    });
  });

  // Обработчик события клика по мастеру
  $('#master-panel .fic').click(function () {
    selectedMasterId = $(this).data('id');
    if (!selectedSalonId || !selectedServiceId || !selectedMasterId) return;

    // Отправляем выбранные значения на сервер
    $.ajax({
      url: '/serviceFinally/', // URL для проверки и редиректа
      method: 'POST',
      data: {
        csrfmiddlewaretoken: $('[name=csrfmiddlewaretoken]').val(), // Передача CSRF-токена
        salon_id: selectedSalonId,
        service_id: selectedServiceId,
        master_id: selectedMasterId,
      },
      success: function (response) {
        if (response.status === 'ok') {
          window.location.href = response.redirect_url; // Переходим на следующую страницу
        } else {
          alert('Ошибка: ' + response.message);
        }
      },
      error: function (xhr, status, error) {
        console.error(error);
      }
    });
  });

  // Функция обновления панели с мастерами (с фото)
  function updateMastersPanel(masters) {
    let content = '';
    masters.forEach((master) => {
      // Добавляем тег img для отображения фото мастера
      const masterPhotoUrl = master.photo ? master.photo : ''; // Если нет фото, будет пустая строка
      content += `
        <div class="accordion__block accordion__block_salon fic">
          ${masterPhotoUrl ? `<img src="${masterPhotoUrl}" alt="Фото мастера" class="master-photo">&nbsp;&nbsp;&nbsp;&nbsp;` : ''}
          <div class="accordion__block_intro">${master.full_name}</div>
          <div class="accordion__block_address">${master.specialty}</div>
        </div>
      `;
    });
    $('#master-panel').html(content);
  }
});