let countdownInterval;

export function initTooltip() {
  $(document).on("mouseenter", ".upper .button, .downer .button", function () {
    const tableNum = $(this).data("table-num");
    clearInterval(countdownInterval);

    const updatePosition = (e) =>
      $("#time-display").css({ left: e.pageX + 15, top: e.pageY + 15 }).show();

    $(document).on("mousemove.tooltip", ".upper .button, .downer .button", updatePosition);

    $.get(`/api/tables/${tableNum}`, (res) => {
      if (!res.success) return;
      const table = res.table;
      const endTime = table.time ? new Date(table.time) : null;

      const tick = () => {
        const remain =
          endTime && endTime > new Date()
            ? new Date(endTime - new Date()).toISOString().substr(11, 8)
            : "만료";

        $("#time-display").text(
          `테이블 ${table.tableNum} | ${table.occupied ? "예약됨" : "빈자리"} | 사용자: ${table.user_name || "-"} | 남은시간: ${remain}`
        );
      };

      tick();
      countdownInterval = setInterval(tick, 1000);
    });
  });

  $(document).on("mouseleave", ".upper .button, .downer .button", () => {
    $("#time-display").hide();
    clearInterval(countdownInterval);
    $(document).off("mousemove.tooltip", ".upper .button, .downer .button");
  });
}
