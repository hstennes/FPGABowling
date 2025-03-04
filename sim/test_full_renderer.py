import cocotb
import os
import random
import sys
import logging
from pathlib import Path
from float_utils import *
from cocotb.clock import Clock
from cocotb.triggers import Timer, ClockCycles, RisingEdge, FallingEdge, ReadOnly
from cocotb.utils import get_sim_time as gst
from cocotb.runner import get_runner
from PIL import Image

def decode_pixel(encoded):
    try:
        encoded = encoded.integer
        return (encoded & 0xFF0000) >> 16, (encoded & 0x00FF00) >> 8, (encoded & 0x0000FF)
    except:
        return (0, 0, 0)

@cocotb.test()
async def test_full_renderer(dut):
    """cocotb test?"""
    im_output = Image.new('RGB', (640, 360))

    dut._log.info("Starting...")
    cocotb.start_soon(Clock(dut.aclk, 10, units="ns").start())
    await ClockCycles(dut.aclk, 3)
    dut.aresetn.value = 1
    await ClockCycles(dut.aclk, 3)
    dut.aresetn.value = 0
    # dut.sphere.value = make_binary_vector_32([0.0, 0.0, 0.0, 0, -5, -5])
    dut.sphere.value = 0x00000000000000000000000000000000c0a00000c0a00000
    dut.pixel_axis_tready.value = 1
    # cylinders = []
    # for i in range(-22, -3, 2):
    #     cylinders.extend([0, 1, 0, 0, -5, i])
    # print(cylinders, len(cylinders))

    cylinders = [0, 1, 0, -6, -5, -16, 0, 1, 0, -2, -5, -16, 0, 1, 0, 2, -5, -16, 0, 1, 0, 6, -5, -16, 0, 1, 0, -4, -5, -14, 0, 1, 0, 0, -5, -14, 0, 1, 0, 4, -5, -14, 0, 1, 0, -2, -5, -12, 0, 1, 0, 2, -5, -12, 0, 1, 0, 0, -5, -10]
    # dut.cylinders.value = make_binary_vector_32(cylinders)
    dut.cylinders.value = 0x3f80000000000000c0c00000c0a00000c1800000000000003f80000000000000c0000000c0a00000c1800000000000003f8000000000000040000000c0a00000c1800000000000003f8000000000000040c00000c0a00000c1800000000000003f80000000000000c0800000c0a00000c1600000000000003f8000000000000000000000c0a00000c1600000000000003f8000000000000040800000c0a00000c1600000000000003f80000000000000c0000000c0a00000c1400000000000003f8000000000000040000000c0a00000c1400000000000003f8000000000000000000000c0a00000c1200000

    print(len(hex(make_binary_vector(cylinders))))

    print(hex(make_binary_vector_32(cylinders)), len(hex(make_binary_vector_32(cylinders))))

    dut.hcount_axis_tdata.value = 0
    dut.vcount_axis_tdata.value = 0
    await ClockCycles(dut.aclk, 500)

    for y in range(195, 295):
        print("Row", y)
        for x in range(260, 390):
            while not dut.hcount_axis_tready.value:
                if dut.pixel_axis_tvalid == 1:
                    im_output.putpixel((dut.hcount_out.value.integer, dut.vcount_out.value.integer), decode_pixel(dut.pixel_axis_tdata.value))
                await ClockCycles(dut.aclk, 1)

            if dut.pixel_axis_tvalid == 1:
                im_output.putpixel((dut.hcount_out.value.integer, dut.vcount_out.value.integer), decode_pixel(dut.pixel_axis_tdata.value))
            dut.hcount_axis_tdata.value = x
            dut.hcount_axis_tvalid.value = 1
            dut.vcount_axis_tdata.value = y
            dut.vcount_axis_tvalid.value = 1
            await ClockCycles(dut.aclk, 1)

    im_output.save('output.png','PNG')

def runner():
    """Simulate the counter using the Python runner."""
    hdl_toplevel_lang = os.getenv("HDL_TOPLEVEL_LANG", "verilog")
    sim = os.getenv("SIM", "icarus")
    proj_path = Path(__file__).resolve().parent.parent
    sys.path.append(str(proj_path / "sim" / "model"))
    sources = [proj_path / "hdl" / "full_renderer.sv"] #grow/modify this as needed.
    sources.append(proj_path / "hdl" / "float_add.sv")
    sources.append(proj_path / "hdl" / "float_mul.sv")
    sources.append(proj_path / "hdl" / "float_div.sv")
    sources.append(proj_path / "hdl" / "float_sqrt.sv")
    sources.append(proj_path / "hdl" / "float_lt.sv")
    sources.append(proj_path / "hdl" / "float_min.sv")
    sources.append(proj_path / "hdl" / "axi_pipe.sv")
    sources.append(proj_path / "hdl" / "vec_add.sv")
    sources.append(proj_path / "hdl" / "vec_dot.sv")
    sources.append(proj_path / "hdl" / "quadratic.sv")
    sources.append(proj_path / "hdl" / "float_mul_pow2.sv")
    sources.append(proj_path / "hdl" / "float_fused_mul_add.sv")
    sources.append(proj_path / "hdl" / "float_sum3.sv")
    sources.append(proj_path / "hdl" / "vec_mul.sv")
    sources.append(proj_path / "hdl" / "vec_clamp.sv")
    sources.append(proj_path / "hdl" / "vec_to_pixel_color.sv")
    sources.append(proj_path / "hdl" / "float_to_fixed.sv")
    sources.append(proj_path / "hdl" / "fixed_to_float.sv")
    sources.append(proj_path / "hdl" / "float_clamp.sv")
    sources.append(proj_path / "hdl" / "vec_fused_mul_add.sv")
    sources.append(proj_path / "hdl" / "vec_norm.sv")
    sources.append(proj_path / "hdl" / "ray_intersect.sv")
    sources.append(proj_path / "hdl" / "ray_from_pixel.sv")
    sources.append(proj_path / "hdl" / "hit_point.sv")
    sources.append(proj_path / "hdl" / "lambert.sv")
    sources.append(proj_path / "hdl" / "float_argmin.sv")
    sources.append(proj_path / "hdl" / "float_multi_argmin.sv")
    sources.append(proj_path / "hdl" / "check_objects.sv")
    sources.append(proj_path / "hdl" / "xilinx_true_dual_port_read_first_2_clock_ram.v")
    build_test_args = ["-Wall"]#,"COCOTB_RESOLVE_X=ZEROS"]
    parameters = {} #!!! nice figured it out.
    sys.path.append(str(proj_path / "sim"))
    runner = get_runner(sim)
    runner.build(
        sources=sources,
        hdl_toplevel="full_renderer",
        always=True,
        build_args=build_test_args,
        parameters=parameters,
        timescale = ('1ns','1ps'),
        waves=True
    )
    run_test_args = []
    runner.test(
        hdl_toplevel="full_renderer",
        test_module="test_full_renderer",
        test_args=run_test_args,
        waves=True
    )

if __name__ == "__main__":
    runner()

# 0000000000000000 0000000000000000 bff5183f99f3dc86 0000000000000000 0000000000000000 4014000000000000

# 0000000000000000 0000000000000000 bff693e93e478e5f 0000000000000000 0000000000000000 4014000000000000

# 0000000000000000 0000000000000000 4014000000000000

# 0000000000000000 4014000000000000 4014000000000000

# c019f8499af611f4 c00066eb1e807723 c02f014bcc4129da

# c019f8499af611f4 40079914e17f88dd c025014bcc4129da

# c019f8499af611f4 40079914e17f88dd c025014bcc4129da

# bfdf8499af611f40 0000000000000000 3fdfd68677dac4c0

'''
3f800000
00000000
c0c00000
c0a00000
c1800000
00000000
3f800000
00000000
c0000000
c0a00000
c1800000
00000000
3f800000
00000000
40000000
c0a00000
c1800000
00000000
3f800000
00000000
40c00000
c0a00000
c1800000
00000000
3f800000
00000000
c0800000
c0a00000
c1600000
00000000
3f800000
00000000
00000000
c0a00000
c1600000
00000000
3f800000
00000000
40800000
c0a00000
c1600000
00000000
3f800000
00000000
c0000000
c0a00000
c1400000
00000000
3f800000
00000000
40000000
c0a00000
c1400000
00000000
3f800000
00000000
00000000
c0a00000
c1200000
'''