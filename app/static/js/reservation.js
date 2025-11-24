export function reserveTable(tableNum) {
  if (!tableNum) {
    alert("테이블 번호를 입력해주세요.");
    return;
  }

  $.ajax({
    type: "PUT",
    url: "/api/tables/me",
    data: JSON.stringify({ tableNum: tableNum }),
    contentType: "application/json",
    success: function (response) {
      alert(`테이블 ${tableNum} 예약이 완료되었습니다!`);
      updateStatusDisplay();
    },
    error: function (xhr) {
      handleAjaxError(xhr);
    },
  });
}

export function cancelTable() {
    $.ajax({
        type: "DELETE",
        url: "/api/tables/me",
        success: function () {
            alert(`예약이 취소되었습니다!`);
            updateStatusDisplay();
        },
        error: function (xhr) {
            handleAjaxError(xhr);
        },
    });
}

function updateStatusDisplay() {
    $.get("/", function (html) {
        const newStatus = $(html).find("#status").html();
        $("#status").html(newStatus);
    });
}

function handleAjaxError(xhr) {
  
  let message = "알 수 없는 오류가 발생했습니다.";

  // 서버가 JSON 반환했을 경우
  if (xhr.responseText) {
    try {
      const response = JSON.parse(xhr.responseText);
      if (response.message) {
        message = response.message;
      }
    } catch (e) {
    }
  }

  if (xhr.status === 400) {
    alert(message); // 클라이언트 잘못 (e.g. 이미 예약됨 등)
  } else if (xhr.status === 500) {
    alert(message); // 서버 오류
  } else {
    alert(message); // 나머지 예상치 못한 오류
  }
}
