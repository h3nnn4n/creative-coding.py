from lib.context_manager import ContextManager
from lib.vector_field_brush import VectorFieldBrush


def main():
    context = ContextManager()
    bf_brush = VectorFieldBrush(context=context)
    bf_brush.circle(
        context.width / 2,
        context.height / 2,
        50,
        (0, 0, 255)
    )

    context.save('vf_brush.png')


if __name__ == '__main__':
    main()
