`timescale 1ns / 1ps
`default_nettype none

module axi_pipe #(parameter SIZE=32, LATENCY=12) (
  input wire [SIZE-1:0] s_axis_a_tdata,
  output logic s_axis_a_tready,
  input wire s_axis_a_tvalid,
  output logic [SIZE-1:0] m_axis_result_tdata,
  input wire m_axis_result_tready,
  output logic m_axis_result_tvalid,
  input wire aclk,
  input wire aresetn);

  logic [SIZE-1:0] a_pipe [LATENCY-1:0];
  logic valid_pipe [LATENCY-1:0];
  logic can_advance;

  always_comb begin
    m_axis_result_tvalid = valid_pipe[LATENCY-1];
    m_axis_result_tdata = a_pipe[LATENCY-1];
    can_advance = m_axis_result_tready || !m_axis_result_tvalid;
    s_axis_a_tready = can_advance;
  end

  always_ff @(posedge aclk) begin
    if(~aresetn) begin
      for(int i = 0; i < LATENCY; i++) begin
        valid_pipe[i] <= 0;
        a_pipe[i] <= 0;
      end
    end
    if(can_advance) begin
      a_pipe[0] <= s_axis_a_tdata;
      valid_pipe[0] <= s_axis_a_tvalid;
      for(int i = 1; i < LATENCY; i++) begin
        a_pipe[i] <= a_pipe[i-1];
        valid_pipe[i] <= valid_pipe[i-1];
      end
    end
  end

endmodule
`default_nettype wire