from context_manager import ContextManager


def main():
    context = ContextManager()

    ctx = context.ctx

    color_a = (178, 34, 34)
    color_b = (64, 224, 208)

    for x in range(0, context.width):
        color = context.lerp_rgb(color_a, color_b, x / context.width, mode='lch')
        context.set_source_rgb(color)
        ctx.move_to(x, 0)
        ctx.line_to(x, context.height / 2)
        ctx.stroke()

        color = context.lerp_rgb(color_a, color_b, x / context.width, mode='rgb')
        context.set_source_rgb(color)
        ctx.move_to(x, context.height / 2)
        ctx.line_to(x, context.height)
        ctx.stroke()

    context.save('color_test.png')

if __name__ == '__main__':
    main()
