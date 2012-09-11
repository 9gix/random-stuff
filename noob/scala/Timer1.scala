object Timer
{
    def rpm(): Unit =
    {
        while (true)
        {
            System.out.println("Hello World")
            Thread.sleep(1000)
        }
    }

    def main(args: Array[String]): Unit =
    {
        rpm()
    }
}
