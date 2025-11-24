from mani_skill.examples.demo_robot import main, Args
import yam
import tyro
if __name__ == "__main__":
    args = tyro.cli(Args)
    main(args)