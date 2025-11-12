let currentStep = 1;

/* STEP NAVIGATION */
$(".next-btn").click(function () {
  if (!$("#cvForm").valid()) return;

  $("#step-" + currentStep).addClass("d-none");
  currentStep++;
  $("#step-" + currentStep).removeClass("d-none");

  $(".step").removeClass("active");
  $('.step[data-step="' + currentStep + '"]').addClass("active");

  // Step 6: Generate summary & projects TOGETHER
  if (currentStep === 6) {
    generateAIContent();
  }
});

/* BACK BUTTON */
$(".back-btn").click(function () {
  $("#step-" + currentStep).addClass("d-none");
  currentStep--;
  $("#step-" + currentStep).removeClass("d-none");

  $(".step").removeClass("active");
  $('.step[data-step="' + currentStep + '"]').addClass("active");
});

/* HIDE WORK FIELDS */
$("#exp_have").change(function () {
  if ($(this).val() === "No") {
    $("#exp_years, #exp_type, #exp_role, #exp_company")
      .closest(".mb-3").hide();
  } else {
    $("#exp_years, #exp_type, #exp_role, #exp_company")
      .closest(".mb-3").show();
  }
});

/* MAIN AI CALL (Summary + Projects) */
function generateAIContent() {

  $("#loaderBox").removeClass("d-none");
  $("#summarySuggestions").addClass("d-none");
  $("#projectSuggestions").addClass("d-none");

  let formData = new FormData($("#cvForm")[0]);

  $.ajax({
    url: "/cv_maker/",
    type: "POST",
    data: formData,
    processData: false,
    contentType: false,

    success: function (response) {

      $("#loaderBox").addClass("d-none");

      // BOTH summary + project are received together
      showSummaryChoices(response.summaries);
      showProjectChoices(response.projects);
    },

    error: function () {
      $("#loaderBox").addClass("d-none");
      alert("Generation failed!");
    }
  });
}

/* SUMMARY OPTIONS */
function showSummaryChoices(list) {
  $("#summaryOptions").empty();
  $("#summarySuggestions").removeClass("d-none");

  list.forEach(text => {
    $("#summaryOptions").append(`
            <div class="summary-choice card p-2 my-2" data-value="${text}">
                <p>${text}</p>
            </div>
        `);
  });
}

/* SELECT SUMMARY */
$(document).on("click", ".summary-choice", function () {
  $(".summary-choice").removeClass("selected");
  $(this).addClass("selected");
  $("#summary").val($(this).data("value"));
});

/* PROJECT OPTIONS */
function showProjectChoices(list) {
  $("#projectOptions").empty();
  $("#projectSuggestions").removeClass("d-none");

  list.forEach(text => {
    $("#projectOptions").append(`
            <div class="project-choice card p-2 my-2" data-value="${text}">
                <p>${text.replace(/\n/g, "<br>")}</p>
            </div>
        `);
  });
}

/* SELECT PROJECT */
$(document).on("click", ".project-choice", function () {
  $(".project-choice").removeClass("selected");
  $(this).addClass("selected");
  $("#final_projects").val($(this).data("value"));
});

/* CARD STYLE */
$("<style>")
  .prop("type", "text/css")
  .html(`
        .summary-choice, .project-choice {
            cursor: pointer;
            border-left: 4px solid transparent;
            transition: 0.2s;
        }
        .summary-choice.selected, .project-choice.selected {
            border-left: 4px solid #0d6efd;
            background: #eaf3ff;
        }
    `)
  .appendTo("head");

/* ==========================================================
 PREVIEW GENERATION FUNCTION
==========================================================*/
function generatePreview() {
  const name = $("#full_name").val();
  const email = $("#email").val();
  const phone = $("#phone").val();
  const address = $("#address").val();
  const summary = $("#summary").val();
  const finalProjects = $("#final_projects").val();
  const edu_level = $("#edu_level").val();
  const edu_field = $("#edu_field").val();
  const edu_college = $("#edu_college").val();
  const edu_year = $("#edu_year").val();
  const edu_cgpa = $("#edu_cgpa").val();
  const skills = $("#skills").val();
  const exp_have = $("#exp_have").val();
  const exp_years = $("#exp_years").val();
  const exp_type = $("#exp_type").val();
  const exp_role = $("#exp_role").val();
  const exp_company = $("#exp_company").val();

  let photoHTML = "";
  const file = $("#photo")[0].files[0];

  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      photoHTML = `<img src="${e.target.result}" class="profile-photo">`;
      render();
      sendToBackend();
    };
    reader.readAsDataURL(file);
  } else {
    render();
    sendToBackend();
  }

  function render() {
    $("#cvPreview").html(`
            <div class='row'>
                <div class='col-3'>${photoHTML}</div>
                <div class='col-9'>
                    <h2>${name}</h2>
                    <p>${email} | ${phone}</p>
                    <p class='text-muted'>${address}</p>
                </div>
            </div><hr>

            <div class='section-title'>Summary</div>
            <p>${summary}</p>

            <div class='section-title'>Education</div>
            <p><strong>${edu_level}</strong> in ${edu_field}</p>
            <p><strong>${edu_college}</strong></p>
            <p>Passing Year: ${edu_year}</p>
            ${edu_cgpa ? `<p>CGPA: ${edu_cgpa}</p>` : ""}

            <div class='section-title'>Skills</div>
            ${skills.map(s => `<span class="badge bg-primary me-1">${s.trim()}</span>`).join("")}

            <div class='section-title'>Projects</div>
            <p>${finalProjects.replace(/\n/g, "<br>")}</p>

            <div class='section-title'>Work Experience</div>
            ${exp_have === "No"
        ? "<p>No Work Experience</p>"
        : `
                <p><strong>Years:</strong> ${exp_years}</p>
                <p><strong>Type:</strong> ${exp_type}</p>
                <p><strong>Role:</strong> ${exp_role}</p>
                <p><strong>Company:</strong> ${exp_company}</p>
            `}
        `);
  }

  function sendToBackend() {
    const formData = new FormData();
    formData.append("full_name", name);
    formData.append("email", email);
    formData.append("phone", phone);
    formData.append("address", address);
    formData.append("summary", summary);
    formData.append("final_projects", finalProjects);
    formData.append("edu_level", edu_level);
    formData.append("edu_field", edu_field);
    formData.append("edu_college", edu_college);
    formData.append("edu_year", edu_year);
    formData.append("edu_cgpa", edu_cgpa);
    formData.append("skills", skills.join(", "));
    formData.append("exp_have", exp_have);
    formData.append("exp_years", exp_years);
    formData.append("exp_type", exp_type);
    formData.append("exp_role", exp_role);
    formData.append("exp_company", exp_company);

    if (file) {
      formData.append("photo", file);
    }

    $("#downloadPdf").click(function () {
      // Collect all data from the CV form
      const formData = new FormData($("#cvForm")[0]);

      // Send POST request to backend to generate PDF
      // $.ajax({
      //   url: "/cv_download/",
      //   type: "POST",
      //   data: formData,
      //   processData: false,
      //   contentType: false,
      //   xhrFields: { responseType: "blob" }, // Expect a PDF blob
      //   success: function (blob, status, xhr) {
      //     // Create downloadable link
      //     const filename = xhr.getResponseHeader("Content-Disposition")
      //       ?.split("filename=")[1] || "My_CV.pdf";

      //     const link = document.createElement("a");
      //     link.href = window.URL.createObjectURL(blob);
      //     link.download = filename.replace(/"/g, "");
      //     document.body.appendChild(link);
      //     link.click();
      //     document.body.removeChild(link);
      //   },
      //   error: function (xhr) {
      //     console.error("Error:", xhr.responseText);
      //     alert("Error generating CV. Please try again.");
      //   }
      // });
  $.ajax({
    url: "/cv_download/",
    type: "POST",
    data: formData,
    processData: false,
    contentType: false,
    success: function (data) {
      if (data.status === "success") {
        // 1️⃣ Show PDF link in the preview div
        $("#cvPreview").html(`
          <p>Your CV is ready! <a href="${data.cv_link}" target="_blank">View PDF</a></p>
        `);

        // 2️⃣ Show the Download PDF button and set click
        $("#downloadPdf")
          .removeClass("d-none")
          .off("click") // remove any previous click handlers
          .on("click", function () {
            window.open(data.cv_link, "_blank"); // open in new tab
          });
      } else {
        alert("Failed to generate CV: " + (data.message || "Unknown error"));
      }
    },
    error: function (xhr) {
      console.error("Error:", xhr.responseText);
      alert("Error generating CV. Please try again.");
    }
  });

    });

  }
}

/* ==========================================================
 FORM SUBMIT → PREVIEW
==========================================================*/
$("#cvForm").submit(function (e) {
  e.preventDefault();

  // Check if summary selected
  if ($("#summary").val().trim() === "") {
    alert("Please select a summary first.");
    return;
  }

  // Check if project description selected
  if ($("#final_projects").val().trim() === "") {
    alert("Please select a project description first.");
    return;
  }

  // Generate full CV preview
  generatePreview();

  // Move step indicator visually
  $(".step").removeClass("active");
  $('.step[data-step="6"]').addClass("active");

  // Show PDF download button
  $("#downloadPdf").removeClass("d-none");
});



/* PDF DOWNLOAD */
// $("#downloadPdf").click(function () {
//   const downloadUrl = "/cv_download/";

//   // Trigger file download
//   window.location.href = downloadUrl;
// });

/* VALIDATION */
// /static/assets/js/app.js

$(document).ready(function () {

  // Initialize jQuery Validation
  $("#cvForm").validate({
    rules: {
      full_name: { required: true, minlength: 3 },
      email: { required: true, email: true },
      phone: { required: true, digits: true, minlength: 10 },
      address: { required: true },

      summary: { required: true, minlength: 10 },
      final_projects: { required: true, minlength: 15 },

      edu_level: { required: true },
      edu_field: { required: true },
      edu_college: { required: true },
      edu_year: { required: true },

      skills: { required: true },

      exp_have: { required: true },
      exp_years: { required: true },
      exp_type: { required: true },
      exp_role: { required: true },
      exp_company: { required: true },
    },

    // Bootstrap-compatible validation styling
    errorClass: "is-invalid",
    validClass: "is-valid",
    errorElement: "div",
    errorPlacement: function (error, element) {
      error.addClass("invalid-feedback");
      if (element.parent(".input-group").length) {
        error.insertAfter(element.parent());
      } else {
        error.insertAfter(element);
      }
    },
    highlight: function (element, errorClass, validClass) {
      $(element).addClass(errorClass).removeClass(validClass);
    },
    unhighlight: function (element, errorClass, validClass) {
      $(element).removeClass(errorClass).addClass(validClass);
    }
  });

});


