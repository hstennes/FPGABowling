`timescale 1ns / 1ps
`default_nettype none

module pins (
    input wire clk_in,                    
    input wire rst_in,
    input wire valid_in,
    input wire [9:0] [15:0] pins_vx_in, 
    input wire [9:0] [15:0] pins_vy_in, 
    input wire [9:0] pins_hit_in,
    output logic [9:0] [10:0] pins_x,     
    output logic [9:0] [9:0] pins_y,  
    output logic [9:0] [15:0] pins_vx_out,     
    output logic [9:0] [15:0] pins_vy_out
);

    // Physics constants
    parameter FRICTION = 0;        // Frictional deceleration in mm/s^2

    parameter PINS_X_INITIAL = 0;
    parameter PINS_Y_INITIAL = 0;
    parameter SCREEN_HEIGHT = 768;
    parameter SCREEN_WIDTH = 1024;
    parameter TIMER_RST = 3000000;


    // Pin dynamics
    // logic [15:0] simtime;              // Simulation time in ms
    logic [9:0] [15:0] pins_vx;
    logic [9:0] [15:0] pins_vy;
    logic [31:0] timer;

    always @(posedge clk_in) begin
        if (rst_in) begin
            pins_vx_out <= 0;
            pins_vy_out <= 0;
            pins_x[0] = SCREEN_WIDTH - 200; pins_y[0] = 300 + 84;  
            pins_x[1] = SCREEN_WIDTH - 160; pins_y[1] = 280 + 84;  
            pins_x[2] = SCREEN_WIDTH - 160; pins_y[2] = 320 + 84;  
            pins_x[3] = SCREEN_WIDTH - 120; pins_y[3] = 260 + 84;  
            pins_x[4] = SCREEN_WIDTH - 120; pins_y[4] = 300 + 84;  
            pins_x[5] = SCREEN_WIDTH - 120; pins_y[5] = 340 + 84;  
            pins_x[6] = SCREEN_WIDTH - 80; pins_y[6] = 240 + 84;  
            pins_x[7] = SCREEN_WIDTH - 80; pins_y[7] = 280 + 84;  
            pins_x[8] = SCREEN_WIDTH - 80; pins_y[8] = 320 + 84;  
            pins_x[9] = SCREEN_WIDTH - 80; pins_y[9] = 360 + 84;  

        end else if (valid_in) begin
            for (int i=0; i<10; i=i+1) begin
                if (pins_hit_in[i] && (pins_x[i] < SCREEN_WIDTH) && (pins_y[i] < SCREEN_HEIGHT)) begin
                    pins_vx_out[i] <= pins_vx_in - FRICTION;
                    pins_vy_out[i] <= pins_vy_in - FRICTION;
                    pins_x[i] <= pins_x[i] + pins_vx_in[i];
                    pins_y[i] <= pins_y[i] + pins_vy_in[i];
                end
            end
        end


            
        // end else if (valid_in) begin
        //     // simtime <= simtime + TIME_STEP;
        //     for (int i=0; i<10; i=i+1) begin
        //         if (pins_hit_in[i]) begin
        //             pins_vx_out[i] <= pins_vx_in - FRICTION * TIME_STEP;
        //             pins_vy_out[i] <= pins_vy_in - FRICTION * TIME_STEP;
        //             pins_x[i] <= pins_x[i] + (pins_vx_in[i] * TIME_STEP) / 1000;
        //             pins_y[i] <= pins_y[i] + (pins_vy_in[i] * TIME_STEP) / 1000;
        //         end
        //     end
        // end
    end

endmodule
