type Props = {};
const Footer = (props: Props) => {
  return (
    <footer className="bg-gray-900 text-white py-3">
      <div className="container mx-auto flex flex-col items-center">
        <div className="flex flex-row">
          <p className="text-lg mr-5">Contact me:</p>
          <a
            href="mailto:ausrys.mikoliunas@gmail.com"
            className="text-blue-400 hover:underline my-1"
          >
            ausrys.mikoliunas@gmail.com
          </a>
        </div>

        <div className="flex flex-row">
          <p className="text-lg mr-5">GitHub:</p>
          <a
            href="https://github.com/ausrys/colorie_counter"
            className="text-blue-400 hover:underline my-1"
          >
            https://github.com/ausrys
          </a>
        </div>
      </div>
    </footer>
  );
};
export default Footer;
