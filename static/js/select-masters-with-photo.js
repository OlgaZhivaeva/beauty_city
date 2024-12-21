$(document).ready(function() {
  let selectedSalonId = null;  // Переменная для хранения id выбранного салона

  // Обработчик события клика по кнопкам выбора салона
  $('#salon-panel .accordion__block').click(function () {
    selectedSalonId = $(this).data('id');
    $('#select-service-btn').prop('disabled', false); // Активируем кнопку выбора услуги
  });

  // Обработчик события клика по услугам
  $('.accordion__block_item').click(function () {
    const serviceId = $(this).data('id'); // Извлекаем id услуги
    if (!selectedSalonId || !serviceId) return;

    $.ajax({
      url: '/get_masters/', // URL для получения мастеров
      method: 'GET',
      data: {
        salon_id: selectedSalonId,
        service_id: serviceId,
      },
      success: function (response) {
        updateMastersPanel(response.masters);
      },
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
