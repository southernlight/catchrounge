import { clickedTable, getChosenTable } from "./table-selection.js";
import { reserveTable, cancelTable } from "./reservation.js";
import { initTooltip } from "./table-tooltip.js";
import { initSocket } from "./websocket.js";

$(document).ready(() => {
  $(".upper .button, .downer .button").on("click", function () {
    clickedTable(this);
  });

  const username = $("#user-data").data("username");

  // 예약 완료 버튼 클릭 시
  $("#complete-button").on("click", function () {
    const tableNum = getChosenTable();
    if (tableNum) {
      reserveTable(tableNum);
    } else {
      alert("테이블을 선택해주세요.");
    }
  });

  $("#leave-button").on("click", function () {
    cancelTable();
  });

  initSocket(username);
  initTooltip();
});
