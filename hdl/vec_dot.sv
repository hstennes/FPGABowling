`timescale 1ns / 1ps
`default_nettype none

module vec_dot #(parameter SIZE) (
  input wire [2:0][SIZE-1:0] s_axis_a_tdata,
  output logic s_axis_a_tready,
  input wire s_axis_a_tvalid,
  input wire [2:0][SIZE-1:0] s_axis_b_tdata,
  output logic s_axis_b_tready,
  input wire s_axis_b_tvalid,
  output logic [SIZE-1:0] m_axis_result_tdata,
  input wire m_axis_result_tready,
  output logic m_axis_result_tvalid,
  input wire aclk,
  input wire aresetn);

  //TOTAL LATENCY: 33

  logic [SIZE-1:0] mul_1_result;
  logic mul_1_valid;

  logic [SIZE-1:0] mul_2_result;
  logic mul_2_valid;

  logic [SIZE-1:0] mul_3_result;
  logic mul_3_valid;

  logic sum_a_ready;
  logic sum_b_ready;
  logic sum_c_ready;
  
  float_mul mul_1(
    .s_axis_a_tdata(s_axis_a_tdata[0]),
    .s_axis_a_tready(s_axis_a_tready),
    .s_axis_a_tvalid(s_axis_a_tvalid),
    .s_axis_b_tdata(s_axis_b_tdata[0]),
    .s_axis_b_tready(s_axis_b_tready),
    .s_axis_b_tvalid(s_axis_b_tvalid),
    .m_axis_result_tdata(mul_1_result),
    .m_axis_result_tready(sum_a_ready),
    .m_axis_result_tvalid(mul_1_valid),
    .aclk(aclk),
    .aresetn(aresetn)
  );

  float_mul mul_2(
    .s_axis_a_tdata(s_axis_a_tdata[1]),
    .s_axis_a_tready(),
    .s_axis_a_tvalid(s_axis_a_tvalid),
    .s_axis_b_tdata(s_axis_b_tdata[1]),
    .s_axis_b_tready(),
    .s_axis_b_tvalid(s_axis_b_tvalid),
    .m_axis_result_tdata(mul_2_result),
    .m_axis_result_tready(sum_b_ready),
    .m_axis_result_tvalid(mul_2_valid),
    .aclk(aclk),
    .aresetn(aresetn)
  );

  float_mul mul_3(
    .s_axis_a_tdata(s_axis_a_tdata[2]),
    .s_axis_a_tready(),
    .s_axis_a_tvalid(s_axis_a_tvalid),
    .s_axis_b_tdata(s_axis_b_tdata[2]),
    .s_axis_b_tready(),
    .s_axis_b_tvalid(s_axis_b_tvalid),
    .m_axis_result_tdata(mul_3_result),
    .m_axis_result_tready(sum_c_ready),
    .m_axis_result_tvalid(mul_3_valid),
    .aclk(aclk),
    .aresetn(aresetn)
  );

  float_sum3 #(.SIZE(SIZE)) sum(
    .s_axis_a_tdata(mul_1_result),
    .s_axis_a_tready(sum_a_ready),
    .s_axis_a_tvalid(mul_1_valid),
    .s_axis_b_tdata(mul_2_result),
    .s_axis_b_tready(sum_b_ready),
    .s_axis_b_tvalid(mul_2_valid),
    .s_axis_c_tdata(mul_3_result),
    .s_axis_c_tready(sum_c_ready),
    .s_axis_c_tvalid(mul_3_valid),
    .m_axis_result_tdata(m_axis_result_tdata),
    .m_axis_result_tvalid(m_axis_result_tvalid),
    .m_axis_result_tready(m_axis_result_tready),
    .aclk(aclk),
    .aresetn(aresetn)
  );

endmodule
`default_nettype wire