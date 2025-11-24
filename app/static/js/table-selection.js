let chosenTable = null;
let selectedButton = null;

export function clickedTable(button) {

  if ($(button).hasClass("bg-red-500")) {
    alert("예약할 수 없습니다. 다른 테이블을 선택해 주세요.");
    return;
  }

  if (selectedButton) {
    $(selectedButton).removeClass("bg-blue-500");
  }

  if (selectedButton === button) {
    selectedButton = null;
    chosenTable = null;
  } else {
    selectedButton = button;
    $(button).addClass("bg-blue-500");
    chosenTable = $(button).data("table-num");
    console.log(`Chosen table number: ${chosenTable}`);
  }
}

export function getChosenTable() {
  return chosenTable;
}
