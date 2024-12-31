$(document).ready(function() {
  let selectedSalonId = null;
  let selectedServiceId = null;
  let selectedMasterId = null;
  let selectedDate = null;
  let selectedTime = null;

  // Обработчик события клика по кнопкам выбора салона
//  $('#salon-panel').on('click','.accordion__block_salon',function() {
  $('#salon-panel .accordion__block_salon').click(function () {
    selectedSalonId = $(this).data('id');
    console.log('Салон:', selectedSalonId );
    $('#select-service-btn').prop('disabled', false); // Активируем кнопку выбора услуги
  });

  // Обработчик события клика по услугам
//  $('#master-panel').on('click', '.accordion__block_salon', function() {
  $('.service__services .accordion__block_item').click(function () {
    selectedServiceId = $(this).data('id'); // Извлекаем id услуги
    console.log('Услуга:', selectedServiceId);
    $('#select-master-btn').prop('disabled', false); // Активируем кнопку выбора мастера
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

    // Делегирование события клика по мастеру
     $('#master-panel').on('click', '.accordion__block_salon', function () {
      selectedMasterId = $(this).data('id');
      console.log('Мастер:', selectedMasterId);
    });

    // Функция обновления панели с мастерами (с фото)
  function updateMastersPanel(masters) {
    let content = '';
    masters.forEach((master) => {
      // Добавляем тег img для отображения фото мастера
      const masterPhotoUrl = master.photo ? master.photo : ''; // Если нет фото, будет пустая строка
        content += `
        <div data-id="${master.id}" class="accordion__block accordion__block_salon fic">
          ${masterPhotoUrl ? `<img src="${masterPhotoUrl}" alt="Фото мастера" class="master-photo">&nbsp;&nbsp;&nbsp;&nbsp;` : ''}
          <div class="accordion__block_intro">${master.full_name}</div>
          <div class="accordion__block_address">${master.specialty}</div>
        </div>
      `;
    });
    $('#master-panel').html(content);
  }



    // Инициализация Datepicker
  const datepicker = new AirDatepicker('#datepickerHere', {
    onSelect: function onSelect({formattedDate}) {
      selectedDate = formattedDate;
      $('#selected_date').val(selectedDate);
      console.log('Дата:', selectedDate);
    },
    minDate: new Date()
  });



    // Обработчик события клика по времени
  $('.time__elems_btn').click(function (e) {
    e.preventDefault()
      selectedTime = $(this).data('time');
      console.log('Время:', selectedTime);
      $('.time__elems_btn').removeClass('active')
      $(this).addClass('active')

  });

    // Обработчик отправки формы
    $('.time__btns_next').on('click', function(event) {
        console.log("Кнопка Далее нажата");
        event.preventDefault();

        console.log('selectedSalonId', selectedSalonId)
        console.log('selectedServiceId', selectedServiceId)
        console.log('selectedMasterId', selectedMasterId)
        console.log('selectedDate', selectedDate)
        console.log('selectedTime', selectedTime)

        if (!selectedSalonId) {
            alert("Пожалуйста, выберите салон!");
             return;
          }
         if (!selectedServiceId) {
            alert("Пожалуйста, выберите услугу!");
             return;
         }
         if (!selectedMasterId) {
           alert("Пожалуйста, выберите мастера!");
           return;
         }
        if (!selectedDate) {
            alert("Пожалуйста, выберите дату!");
             return;
        }
        if (!selectedTime) {
           alert("Пожалуйста, выберите время!");
             return;
        }
        if (!selectedSalonId || !selectedServiceId || !selectedMasterId || !selectedDate || !selectedTime) {
           alert("Пожалуйста, выберите все необходимые параметры!");
            return;
        }
        console.log('Salon ID перед отправкой:', selectedSalonId);
        const formData = {
            salon_id: selectedSalonId,
            service_id: selectedServiceId,
            master_id: selectedMasterId,
            date: selectedDate,
            time: selectedTime
        }
        console.log(formData)

        $.ajax({
              url: '/service_finally/',
              method: 'POST',
              data: JSON.stringify(formData),
              contentType: "application/json",
              headers: {
                  'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
              },
              success: function(response){
                window.location.href = "/service_finally";
              },
              error: function(xhr, textStatus, errorThrown){
                  alert( "Произошла ошибка: " +  textStatus +  "  " + errorThrown)
              }
            });
    });
});